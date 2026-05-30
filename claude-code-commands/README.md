# Claude Code session commands

Seven [Claude Code](https://docs.claude.com/en/docs/claude-code) slash commands I use to run an agent across many projects at once. They share one idea: a **gitignored `plan/` folder** in each repo holding three files —

- `history.md` — Decisions · Log · Dead ends
- `pending.md` — Now · Parked · Open questions
- `workplan.md` — chunked, checkboxed play

The commands read and write those files, so every session picks up exactly where the last one left off.

| Command | When | What it does |
|---------|------|--------------|
| `/scaffold` | new project | Bootstrap from attached handoff materials (md/zip): local folder + git + remote repo + seeded `plan/` + a brief on the first move. |
| `/standup` | start of day | Scan every repo with a `plan/` folder → active / idle / stale, each with its next move. Pick one. |
| `/resume` | start of session | Read the handoff (workplan + pending + history + latest summary + git state), brief you, and wait. Read-only. |
| `/decide "<why>"` | mid-session | Append a dated one-line decision to `history.md`. Captures the *why* before it evaporates. |
| `/forward-pass` | anytime | Fresh-eyes whole-app audit — bugs / security / stray code — that outputs a **batched workplan**, not a findings dump. Writes `plan/forward-pass-<date>.md`. |
| `/windup` | end of session | Day summary + pending + workplan + push + tomorrow's handoff. |
| `/replan` | occasionally | Fold accumulated summaries + scratch back into the three files; archive the rest. |

They speak one vocabulary, so each hands off to the next: `/windup` writes what `/resume` reads, `/forward-pass` feeds `/replan`, `/decide` feeds `history.md`.

## Install

```bash
cp commands/*.md ~/.claude/commands/                 # available in all projects
# or:  cp commands/*.md <project>/.claude/commands/  # just one project
```

The command name is the filename without `.md` (`windup.md` → `/windup`). First run will offer to add `plan/` to your `.gitignore`. If you don't keep repos under `~/code`, set your scan root at the top of `commands/standup.md`.

## The one to try first

`/forward-pass`. Every other review tool looks at your diff; this one reads the whole app cold and hands back an ordered, checkboxed fix-plan with stable finding IDs — the kind of thing you actually work through instead of skim once.
