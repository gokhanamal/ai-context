# Edit Policy

Use this guide after the user approves a destination.

## Core Rule

Nothing is written before approval.

After approval, update one primary destination unless the user explicitly asks for more than one.

## Existing Skill Updates

Apply the mixed policy.

### Auto-Apply After Approval

These are append-only changes that do not alter the skill's core behavior:

- adding a command example
- adding a parameter note
- adding a brief gotcha
- adding a short example
- adding a cross-link to a relevant solution doc

Preferred targets:

- `references/examples.md`
- `references/patterns.md`
- `references/resources.md`

Use `SKILL.md` only when the reusable behavior truly belongs in the core workflow.

### Preview First

Show the exact proposed diff or a concise preview before editing when the change would:

- modify trigger conditions
- rewrite workflow steps
- change the skill's purpose or scope
- add or remove major sections
- replace existing guidance instead of extending it

## New Skill Creation

Create the smallest useful package:

- `<skill-name>/SKILL.md`
- optional `references/` with one focused file if helpful
- README table entry

Use kebab-case for the directory and the `name:` frontmatter. Keep the first version narrow and practical.

## Lessons Updates

Append one concise bullet to `tasks/lessons.md`.

Preferred format:

- `When X is true, do Y instead of Z.`
- `Prefer A in this repo because B.`
- `Do not assume C; verify D first.`

Do not write multi-paragraph lessons.

## Solution Document Updates

Create `docs/solutions/` and category directories on demand.

Use a compact markdown format:

```markdown
---
title: Short title
date: YYYY-MM-DD
category: workflow-issues
---

# Short title

## Problem
[1-2 sentences]

## Root Cause
[1-2 sentences]

## Solution
[1-2 short paragraphs or bullets]

## Prevention
- [One concrete prevention rule]
```

Keep these documents focused. They should explain the pattern, not retell the whole conversation.

## Recommended Search Before Editing

Before applying any approved update, search the destination to avoid duplicate entries or conflicting guidance.

Suggested checks:

- `rg -n "<key phrase>" <target-path>`
- `rg --files <skill-dir>`

## Summary After Writing

After a successful update:

- name the destination that was updated
- reference the edited file paths
- explain the change in one short paragraph
- mention preview-first behavior if the user declined a structural edit
