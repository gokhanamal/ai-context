# Capture

Human-facing overview for the `capture` skill.

## What It Does

This skill helps decide whether a useful insight from the current session should be saved somewhere reusable.

It can recommend:

- updating an existing skill
- creating a new skill
- adding a short rule to `tasks/lessons.md`
- writing a reusable solution doc under `docs/solutions/`
- ignoring the moment if it is too narrow or temporary

## When To Use It

Use this skill after something important becomes clear, for example:

- a fix is confirmed
- a non-obvious command or parameter is corrected
- a team rule or repo preference is established
- someone says "remember this" or "this should be a skill"

## How It Helps

The skill checks whether the insight is actually reusable, looks for duplicates, recommends the best destination, asks for approval, and only writes after approval.

That keeps the knowledge base growing without turning every small moment into noisy documentation.

## Files

- `SKILL.md` - the agent-facing capture workflow
- `references/target-selection.md` - how the skill chooses where knowledge should go
- `references/edit-policy.md` - what can be edited directly versus previewed first
- `references/examples.md` - example trigger moments and recommendation flows
