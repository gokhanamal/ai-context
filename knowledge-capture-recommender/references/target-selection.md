# Target Selection

Use this guide to choose the best destination for a reusable moment.

## Step 1: Confirm the Moment Is Reusable

The moment is usually capture-worthy when it includes at least one of these:

- A corrected command or parameter that is easy to forget
- A repeatable project rule or operating preference
- A confirmed fix with a non-obvious root cause
- A decision that should guide future work in the same domain
- A repeated clarification that another agent would likely need again

Prefer `ignore` when the information is:

- temporary
- highly local to one file edit
- obvious from the code itself
- not likely to repeat

## Step 2: Check for Existing Capture

Before recommending a destination, search for duplicates:

- Search related skill names and reference files with `rg`
- Check `tasks/lessons.md` for an equivalent rule
- Check `docs/solutions/` if it exists

If the insight already exists, recommend updating the existing entry only if the new context materially improves it.

## Step 3: Pick the Destination

### Update Existing Skill

Choose this when:

- The knowledge clearly belongs to an existing domain
- Another agent would benefit during future work in that domain
- The update can be kept concise and reusable

Common examples:

- a correct CLI command
- a parameter gotcha
- a domain-specific example
- a rule that belongs in a skill's references

Strong signals:

- A clear skill name match
- Repeated domain language in the conversation
- The insight fits naturally into `references/examples.md`, `references/patterns.md`, or `references/resources.md`

### Create New Skill

Choose this when:

- The insight starts a new repeatable domain
- Existing skills do not fit cleanly
- Future work will likely revisit the same domain

Use this sparingly. A new skill should represent a reusable area of work, not a single stray fact.

### Add to `tasks/lessons.md`

Choose this when:

- The insight is a short rule or reminder
- It is repo-specific but not a full domain workflow
- Another agent would benefit from seeing it early in future sessions

Good lessons are brief and imperative:

- "When X is true, do Y."
- "Prefer A over B in this repo."
- "Do not assume C; verify D first."

### Add to `docs/solutions/...`

Choose this when:

- The moment captures a fuller problem and solution pattern
- The root cause matters as much as the final rule
- Future readers will need context, not just a reminder

This is the right fit for confirmed fixes, recurring bugs, and compound-style institutional knowledge.

### Ignore

Choose this when:

- The information is too narrow or temporary
- A destination would add noise rather than clarity
- The benefit of capture is low

Be explicit about why the skill recommends no write.

## Confidence Rules

High confidence:

- One destination clearly fits better than the others
- A specific existing skill is an obvious match

Medium confidence:

- Two destinations are plausible
- The knowledge is reusable, but the best home is debatable

Low confidence:

- The moment may not be reusable at all
- The domain fit is weak

When confidence is medium or low, say so and offer alternatives instead of pretending the choice is obvious.

## Tie-Breakers

When two options seem plausible, prefer:

1. `tasks/lessons.md` over a forced skill update
2. an existing skill over creating a new one
3. `docs/solutions/...` over `tasks/lessons.md` when root cause and context matter
4. `ignore` over noisy or speculative capture
