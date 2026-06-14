# Claude Code session commands

Fifteen [Claude Code](https://docs.claude.com/en/docs/claude-code) slash commands I use to run an agent across many projects at once. They share one idea: a **gitignored `plan/` folder** in each repo holding three files —

- `history.md` — Decisions · Log · Dead ends
- `pending.md` — Now · Parked · Open questions
- `workplan.md` — chunked, checkboxed play

The commands read and write those files, so every session picks up exactly where the last one left off.

| Command | When | What it does |
|---------|------|--------------|
| `/scaffold-nt` | new project | Bootstrap from attached handoff materials (md/zip): local folder + git + remote repo + seeded `plan/` + a brief on the first move. |
| `/standup-nt` | start of day | Scan every repo with a `plan/` folder → active / idle / stale, each with its next move. Pick one. |
| `/resume-nt` | start of session | Read the handoff (workplan + pending + history + latest summary + git state), brief you, and wait. Read-only. |
| `/decide-nt "<why>"` | mid-session | Append a dated one-line decision to `history.md`. Captures the *why* before it evaporates. |
| `/idea-nt "<idea>"` | anytime | Park a future-work idea into the backlog (`plan/ideas.md`, or `IDEAS.md` if present) — the `/decide-nt` pattern, for ideas. Friction-free, no derailing the current task. |
| `/forward-pass-nt` | anytime | Fresh-eyes whole-app audit — bugs / security / stray code — that outputs a **batched workplan**, not a findings dump. Writes `plan/forward-pass-<date>.md`. |
| `/walkthrough-nt` | anytime | Live counterpart to `/forward-pass-nt`: identify each user role, drive the running app through their journeys **in a real browser**, catch logical errors as they surface, and **fix them**. Writes `plan/walkthrough-<date>.md`. |
| `/guide-nt` | anytime | Documentation sibling of `/walkthrough-nt`: walk each role's features **in a browser capturing screenshots**, then build a single-file **searchable HTML guide**. Regenerates from a committed generator — never hand-edits the output. |
| `/ux-review-nt` | anytime | Cold-first-timer UX review: wipe all state, walk the app **as a brand-new user**, and report where build-order accretion fails the newcomer (arrival, onboarding, nav/IA) — plus a Lighthouse a11y + perf pass. Read-only; proposes an ideal first-run + IA. Writes `plan/ux-review-<date>.md`. |
| `/execute-nt` | anytime | Work a batched fix-workplan from a `/forward-pass-nt` / `/ux-review-nt` / `/maintain-nt` report — fix + verify each item, check it off, log the SHA, pause between batches. The **executor** for static findings. |
| `/maintain-nt` | upkeep | Maintenance sweep — outdated/deprecated deps, stale GitHub Actions, security advisories, dead links, lockfile drift → a ranked fix-workplan. Read-only (offers safe quick-fixes). Writes `plan/maintenance-<date>.md`. |
| `/release-nt` | launch | Cut a release — suggest a semver bump from the commits, write `CHANGELOG.md`, draft notes, then on confirm tag + push + GitHub release + deploy. The mechanics, where `/package-nt` is the marketing. |
| `/package-nt` | launch | Ship a project to the world — the bookend to `/scaffold-nt`: a deep readiness gate (`/security-review` + `/forward-pass-nt` + a secrets + essentials check), social-framed screenshots (committed to `marketing/`), and drafted X / LinkedIn / Show HN / subreddit collateral (local). **Drafts, never posts.** |
| `/windup-nt` | end of session | Day summary + pending + workplan + push + tomorrow's handoff. |
| `/replan-nt` | occasionally | Fold accumulated summaries + scratch back into the three files; archive the rest. |

They speak one vocabulary, so each hands off to the next: `/windup-nt` writes what `/resume-nt` reads, `/forward-pass-nt` and `/walkthrough-nt` feed `/replan-nt`, `/decide-nt` feeds `history.md`.

## Install

```bash
cp commands/*.md ~/.claude/commands/                 # available in all projects
# or:  cp commands/*.md <project>/.claude/commands/  # just one project
```

The command name is the filename without `.md` (`windup-nt.md` → `/windup-nt`). First run will offer to add `plan/` to your `.gitignore`. If you don't keep repos under `~/code`, set your scan root at the top of `commands/standup-nt.md`.

## The one to try first

`/forward-pass-nt`. Every other review tool looks at your diff; this one reads the whole app cold and hands back an ordered, checkboxed fix-plan with stable finding IDs — the kind of thing you actually work through instead of skim once.
