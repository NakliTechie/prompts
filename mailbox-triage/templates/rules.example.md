# Triage rules

> This file is the accumulated, deployment-specific knowledge — everything
> the generic `mailbox-triage` skill does NOT know on its own. `check` reads
> it every run; `tune` is the only thing that edits it, and only when you
> correct something.

## Priority people (ALWAYS surface, at the top, with a summary)
- **Example: Jane Doe — `jane@example.com`.** Forwards articles; summarize
  the substance, flag any ask.

## Known recurring patterns (apply these; don't re-ask)
- **Example vendor thread** — these are reimbursements TO you, not bills you
  owe. Check the bank alert for the matching amount before flagging as
  unpaid.

## Bank/credit-alert reliability (learned from experience)
- Note here any channel (bank, card, SI/standing-instruction) that does or
  doesn't reliably email a confirmation, so `check` doesn't misread silence
  as non-payment. Absence of an alert is only a signal for channels you've
  confirmed DO normally alert.

## Recurring obligations & expected-inbound (REMIND IF MISSING)
- **Example: rent, due by the 5th, must generate an alert.** If the alert
  hasn't posted by the 5th, that's an immediate REMINDER, not a soft "watch
  for it" item.

## VERIFY before declaring something undone
Before flagging any item as "not sent / not done / no reply / unconfirmed",
search `in:sent` on every connected account for a matching message. An
absent item in the inbox alone is not proof nothing happened.

## Resolved — do NOT re-surface
Dated entries closing out items you confirmed by hand, so `check` stops
raising them. `tune` appends here.

## Never (without your explicit per-item go-ahead)
- Send, reply, forward, or archive/trash anything during `check`.
- Accept calendar invites or click links.
`check` READS and REPORTS. You decide what gets actioned. (A `tune` or a
direct, explicit in-session request — like "forward that to X" — is a
different thing: that's you asking Claude to act, not the automated `check`
routine acting on its own.)
