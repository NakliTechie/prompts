# Triage rules

> This file is the accumulated, deployment-specific knowledge — everything
> the generic `mailbox-triage` skill does NOT know on its own. `check` reads
> it every run; `tune` is the only thing that edits it, and only when you
> correct something. See `SKILL.md`'s "Patterns proven in practice" for the
> methodology this file's entries follow — these are worked examples of
> that methodology, not a complete rules file for any real mailbox.

## Priority people (ALWAYS surface, at the top, WITH a summary)
- **Jane Doe — `jane@example.com`.** Forwards articles and asks several
  times a week; pull the full body (not just the snippet) so the ask
  doesn't get lost in a long forward chain. Summarize the substance, flag
  any ask explicitly.

## Known recurring patterns (apply these; don't re-ask)
- **`billing@vendor-example.com` monthly invoice threads** — these are
  **reimbursements owed TO you**, not bills you pay. Check the matching
  bank-credit alert before flagging as unpaid; never surface as
  "approve/process a payment."
- **`accounts@subcontractor-example.com` invoices, cc'd to you** — payable
  by the party who commissioned the subcontractor, not by you. You're cc'd
  for visibility only. Confirm who actually pays before ever calling this
  an unpaid bill of yours.

## Cost/spend attribution (apply, don't re-ask)
When one shared account's spend covers multiple tenants/projects, split
before reporting:
- **Resource type A, in region X** — yours; report the number, don't treat
  it as unexplained.
- **Resource type B** — not yours; these are the ones to escalate to the
  actual owner, asking whether a known campaign/process explains the spike.

## Bank/credit-alert reliability (learned from experience, dated)
- **2026-08-31 — inbound credits from Bank X are unreliable.** A ~$X
  reimbursement landed and was confirmed against the bank statement, but no
  credit-alert email was ever generated across a wide search. Debit alerts
  fire normally; only credits are silent on this bank. So for expected
  INBOUND money: say "no credit alert seen in email," never "not credited"
  — the statement is the authority, not the inbox.
- **2026-09-07 — a standing-instruction (SI) debit leg doesn't alert either,
  even though it's a real, confirmed debit.** Confirmed by the user against
  their bank statement after an exhaustive search of the alert channel
  found nothing. Don't wait for an email on this specific leg in future
  cycles.

## Recurring obligations & expected-inbound (REMIND IF MISSING)
- **Obligation Z, paid in two legs that must sum to the known total.** If
  only one leg's alert is found and it's short of the total by exactly the
  other leg's usual amount, the other leg is genuinely missing — flag it,
  don't wave it off as "probably fine."
- **Leg A must post by day D, full stop.** Missing by day D is an immediate
  REMINDER, not a soft "watch for it" item — this was explicitly marked
  strict by the user, unlike most obligations below which get a soft
  window.
- **Leg B (see the alert-reliability note above) — don't expect an email
  for this leg at all**; its confirmation is the bank statement, checked
  only when asked, not inferred from silence.

## VERIFY before declaring something undone (important)
Before flagging any item as "not sent / not done / no reply / unconfirmed",
search `in:sent` on every connected account for a matching message. Inbox
-only search gives false negatives — a real example: an escalation email
got reported as "not sent" when it had actually gone out days earlier to
the right people. Absence-in-inbox ≠ not-done.

## Resolved — do NOT re-surface (dated; scoped to the cycle unless noted)
- **2026-09-09 — a scheduled call was cancelled by the other party**, who
  said they'd reschedule after a stated date. Nothing pending on your side
  until after that date.
- **2026-09-09 — a trial the user is not continuing.** No decision to make;
  drop the line entirely rather than re-surfacing "decision needed."

## Never (without your explicit per-item go-ahead)
- Send, reply, forward, or archive/trash anything during `check`.
- Accept calendar invites or click links.
`check` READS and REPORTS. You decide what gets actioned. (A `tune` or a
direct, explicit in-session request — like "forward that to X" — is a
different thing: that's you asking Claude to act, not the automated `check`
routine acting on its own.)
