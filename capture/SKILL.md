---
name: capture
description: This skill should be used when a reusable insight, command, fix, or decision may need to be captured into the right artifact: an existing skill, a new skill, a lesson, or a solution document. It is especially useful after confirmed fixes, finalized decisions, explicit "remember this" moments, or corrected CLI usage.
---

# Capture

Detect when a recent moment is reusable knowledge, recommend the best place to capture it, ask for approval, and then update the approved destination safely.

## Trigger

Activate only when at least one of these is true:

- The user invokes this skill directly
- The conversation includes an explicit capture cue such as:
  - "remember this"
  - "this should be a skill"
  - "we always forget this"
  - "the correct command is"
- A workflow reaches a checkpoint such as:
  - a fix is confirmed
  - a decision is finalized
  - a non-obvious command or parameter is established

Do not activate continuously or speculatively. This skill is a checkpoint helper, not ambient monitoring.

## Instructions

1. Confirm the trigger moment and identify the candidate knowledge from recent context.
2. Read `references/target-selection.md` to decide whether the best destination is:
   - an existing skill
   - a new skill
   - `tasks/lessons.md`
   - `docs/solutions/...`
   - ignore
3. Before recommending a destination, check for an existing capture to avoid duplication.
   - Search matching skills with `rg`
   - Check `tasks/lessons.md`
   - Check `docs/solutions/` if it exists
4. Recommend one destination with a short reason and confidence statement.
   - If confidence is high for an existing skill, name that skill directly.
   - If the decision is ambiguous, present the top two options instead of bluffing certainty.
5. Ask for approval using plain numbered choices so the flow works across platforms.
   - Example:
     1. Approve recommended destination
     2. Choose a different destination
     3. Ignore for now
6. If the user approves a write, read `references/edit-policy.md` and follow the target-specific rules.
   - Existing skill: apply append-only updates directly after approval, but preview structural changes first.
   - New skill: create a minimal skill package plus a README entry.
   - Lessons: append one short rule to `tasks/lessons.md`.
   - Solution docs: create `docs/solutions/` on demand and write one compact solution document.
7. Keep the update focused.
   - Prefer one primary destination per moment.
   - Add cross-links only when they materially help.
   - Do not write to multiple destinations unless the user explicitly asks.
8. Summarize what changed and reference the edited files.

## Guardrails

- Do not write anything before approval.
- Do not force a skill update when a lesson is the cleaner fit.
- Do not rewrite a skill's core workflow without showing a preview first.
- Do not create a new skill for a one-off project fact.
- Do not claim certainty when the destination is genuinely unclear.

## References

- `references/target-selection.md` - destination heuristics, confidence rules, and duplicate checks
- `references/edit-policy.md` - mixed policy for skill edits plus write templates for all destinations
- `references/examples.md` - sample trigger moments, approvals, and destination outcomes
