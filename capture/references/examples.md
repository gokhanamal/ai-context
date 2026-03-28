# Examples

Use these examples to keep the interaction concrete and low-noise.

## Trigger Examples

Manual invocation:

- "Use capture for this fix."

Keyword moments:

- "remember this"
- "this should be a skill"
- "we always forget this"
- "the correct command is `foo --bar baz`"

Checkpoint handoff:

- "The fix is confirmed. Check whether this should be captured."
- "We finalized the decision. See if this belongs in a skill or lessons."

## Example: Update Existing Skill

Context:

- A user corrects a CLI flag and says, "the correct command is `gh pr checks 42`."
- The domain clearly matches a GitHub-related skill.

Recommended response shape:

1. State the recommendation:
   - "This looks reusable. Best fit: update the existing GitHub skill with the correct command example."
2. Give numbered choices:
   - `1. Update the recommended skill`
   - `2. Choose a different destination`
   - `3. Ignore for now`
3. If approved, add the example to the most relevant reference file.

## Example: Add to Lessons

Context:

- A repo-specific rule is established: use repo-root plugin paths instead of scaffolding duplicate plugin folders.

Recommended response shape:

- "This is a short repo rule rather than a domain workflow. Best fit: `tasks/lessons.md`."

## Example: Add to Solution Docs

Context:

- A fix succeeds and the root cause was non-obvious enough that future readers will need both the symptom and the explanation.

Recommended response shape:

- "This looks like a reusable solved problem. Best fit: a compact document under `docs/solutions/...`."

## Example: Create New Skill

Context:

- The same new operational domain appears repeatedly, and no existing skill matches it cleanly.

Recommended response shape:

- "This seems like the start of a new repeatable domain. Best fit: create a new skill with a minimal first version."

## Example: Ignore

Context:

- The information is temporary, obvious from the code, or too narrow to help future sessions.

Recommended response shape:

- "I do not think this is worth capturing yet. Best fit: ignore for now."

## Example Approval Prompt

Use plain numbered choices so the flow works across platforms:

1. Approve recommended destination
2. Choose a different destination
3. Ignore for now

If the recommendation is ambiguous, replace option 1 with two concrete destination options.
