# mailbox-triage

A skill for triaging one or more mailboxes with an agent: read-only checks
that verify before flagging anything as undone, and a rules file that
learns from your corrections instead of forgetting them every session.

Extracted from a few weeks running this by hand on
[inbox-watch](https://github.com/NakliTechie/inbox-watch) — see that repo's
`TRIAGE.md` for what a mature rules file looks like in practice (the
`rules.md` shape here is the generic version of it).

See [`SKILL.md`](SKILL.md) for the actual skill definition (what an agent
reads to run `setup` / `check` / `tune`). This README is just the
human-facing overview.

## Why standalone, not an ntkit command

ntkit's commands are verbs over generic dev artifacts (git, `plan/`, code).
This is a domain-specific engine over live mailboxes with deeply personal
rules (who's a priority sender, what a rent split looks like, which bank
alerts are reliable) — a different kind of thing, so it lives on its own
rather than blurring ntkit's scope.

## Quick start

1. **Cheapest path — claude.ai's native Gmail connector.** If the mailbox
   you want watched can go through that connector and it's the only
   mailbox in this deployment, there's nothing to install: just write a
   `rules.md` (copy `templates/rules.example.md`) and start running
   `check`.
2. **Second mailbox / connector can't reach it — local OAuth:**
   ```bash
   scripts/setup_wizard.sh ~/path/to/your/deployment
   ```
   Walks you through it: reuses an existing OAuth client for the same
   Google Workspace domain if one exists, scripts what `gcloud` can reach,
   and deep-links the handful of console clicks Google requires a human
   for. First mailbox in a new domain: ~3 clicks. Every mailbox after that
   in the same domain: one browser consent click, no console at all.
3. Fill in `rules.md` with your first few real priority-senders and
   recurring-obligation entries. An empty rules file makes `check` no
   smarter than reading raw mail.
4. Run `check` regularly (by hand, or wire it into a scheduled task). When
   it gets something wrong, run `tune` with the correction instead of
   fixing it in your head every time.

## Layout

```
mailbox-triage/
  SKILL.md              the skill definition — start here
  README.md             this file
  requirements.txt       google-api-python-client, google-auth-oauthlib, PyYAML
  scripts/
    auth.py              one-time OAuth, generic (config-driven)
    fetch.py              read-only mailbox fetch, generic (config-driven)
    setup_wizard.sh        interactive local-OAuth setup, minimal-friction
  templates/
    account.example.yaml
    rules.example.md
```
