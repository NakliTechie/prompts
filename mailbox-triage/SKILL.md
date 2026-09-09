# mailbox-triage

**Read-only mailbox triage with a self-correcting rules file.** Watches one
or more mailboxes, cross-checks before flagging anything as undone, and
folds your corrections back into its own knowledge instead of losing them.

This is a standalone skill, not an ntkit command — it operates on live
mailbox data with per-person financial/relationship rules, a different
domain from ntkit's git/`plan/`/code verbs. Install per-project, same as any
other skill: copy this folder (or symlink it) into the project that will
hold the deployment, or point `--deploy-dir` at wherever you want the
account config + rules file to live.

## Verbs

Invoke as `mailbox-triage <verb> [args]`.

- **`setup <deploy-dir>`** — one-time. Wires one mailbox account. Tries the
  free path first (claude.ai's native Gmail connector — zero config, just
  needs the connector enabled in the client); falls back to the local-OAuth
  path (`scripts/setup_wizard.sh`) only when a second account is needed,
  since the native connector is single-account.
- **`check <deploy-dir>`** — read every configured account, apply
  `rules.md`, emit a dated brief. The main loop, run as often as you like
  (manually or via a scheduled task).
- **`tune <deploy-dir> "<correction>"`** — you noticed `check` got something
  wrong or missed a pattern; fold it into `rules.md` so it doesn't happen
  again.

A deployment directory holds:
```
<deploy-dir>/
  account.yaml         # one mailbox's connection + queries (local-OAuth path only)
  client_secret.json   # gitignored, never commit
  token.json           # gitignored, never commit
  rules.md             # the accumulated knowledge — see templates/rules.example.md
  briefs/              # dated output, latest.md always the newest
```
For a connector-backed account there's no `account.yaml`/`client_secret.json`/
`token.json` — `check` reads that mailbox through the connector's own search
tool instead of `scripts/fetch.py`.

## `setup`

1. Ask: does this account have (or can it get) claude.ai's native Gmail
   connector? If yes and it's the only mailbox in this deployment, stop
   here — nothing to install. Note in `rules.md` which connector tool to
   use for `check`.
2. If a second mailbox is needed (the connector is single-account) or the
   account is otherwise unreachable by connector, run
   `scripts/setup_wizard.sh <deploy-dir>`. It:
   - reuses an existing OAuth client under `~/.mailbox-triage/credentials/<domain>.json`
     if this domain has been set up before — no new Google Cloud project;
   - otherwise scripts everything `gcloud` can reach (project create, enable
     `gmail.googleapis.com`, and verifies the enable actually took), then
     prints direct deep-links for the three steps Google requires a human
     for (consent screen, OAuth client creation, JSON download) instead of
     "go to console.cloud.google.com and find it";
   - creates the venv, installs deps, writes `account.yaml`, runs the
     browser consent flow, and smoke-tests with `fetch.py`.
3. Copy `templates/rules.example.md` to `<deploy-dir>/rules.md` if it
   doesn't exist yet, and help the user fill in the first few real
   priority-senders / recurring-obligation entries — an empty rules file
   makes the first few `check` runs no smarter than reading raw mail.

## `check`

1. For each configured account: connector-backed → use that connector's
   search tool with the queries named in `rules.md`; local-OAuth → run
   `scripts/fetch.py <deploy-dir>/account.yaml`.
2. Read `<deploy-dir>/rules.md` in full before triaging anything — every
   classification below defers to it.
3. **Verify before declaring anything undone.** Before writing "not sent /
   not done / no reply / unconfirmed", search `in:sent` on every connected
   account for a matching message. Absence in the inbox alone is not proof
   of non-action — this is the single highest-value check in the whole
   skill; skipping it is the most common false positive.
4. Apply `rules.md`'s recurring-obligation and bank/credit-alert-reliability
   sections: absence of an expected item is a signal only for channels the
   rules file says normally alert; for tags marked as unreliable, silence
   is not a fact.
5. Classify: priority-people items (full body, always surfaced) · new since
   last run · still-open carried items · resolved (drop silently per
   `rules.md`'s Resolved section) · noise (drop, don't list).
6. Write `<deploy-dir>/briefs/<timestamp>.md` and update `latest.md`.
   Worst news first. State which searches were run for anything you're
   asserting absence on.
7. **Never send, reply, forward, label, archive, or trash anything in this
   verb.** Read and report only. A direct, explicit in-session request from
   the user to act on something `check` surfaced (e.g. "forward that to
   X") is a separate action outside this verb — do it, but don't fold it
   into an unattended `check` run.

## `tune`

1. Read the correction. Identify which section of `rules.md` it belongs in:
   a fixed assumption → Known recurring patterns or Recurring obligations;
   a discovered channel quirk (an alert that doesn't fire, or does) → the
   bank/credit-alert-reliability section; a one-off closure ("X is paid,
   stop flagging it") → Resolved, dated.
2. If the correction contradicts something already in `rules.md`, replace
   the wrong claim — don't leave both versions sitting in the file.
3. If verifiable by search (an amount, a sent message, a debit), verify it
   before writing the entry, and cite what you found. If a search comes up
   empty even though the user says something happened, say so plainly in
   the entry rather than silently trusting or silently doubting — note the
   gap so future runs know the channel doesn't corroborate it by email.
4. Write the edit, then hand it back for the user to look at before it's
   treated as settled — `tune` edits a file, it doesn't require a commit or
   a push on its own.

## Design notes

- The skill is the engine; `rules.md` + `account.yaml` are the data. A
  second deployment reuses the scripts and the verbs, never another
  deployment's rules file.
- `fetch.py`/`auth.py` are intentionally generic — every project-specific
  value (queries, priority senders, body-size limits) lives in
  `account.yaml`, not in the scripts.
- Local-OAuth accounts should request the narrowest scope that covers the
  need. `gmail.modify` (read+send, no permanent delete) is the default in
  the template because `tune`-driven follow-ups sometimes need to send —
  but `check` itself must never use the send capability regardless of what
  the token allows; keep that a code-level rule, not just a documented one,
  wherever `check` is automated as an unattended scheduled task.
