# Contributing

Thanks for helping improve this skills repository.

The best contributions here are focused, well-documented, and easy for another agent user to pick up without extra context.

## Ways To Contribute

- Add a new skill with a clear, narrow purpose
- Improve an existing skill's instructions, references, or examples
- Fix packaging, installation, or validation issues
- Improve documentation, templates, or contributor workflows

## Local Workflow

1. Create a branch for the change.
2. Make the smallest change that fully solves the problem.
3. Update docs and packaging metadata alongside the code when names or install paths change.
4. Run the repository validation script:

```bash
python3 scripts/validate_repo.py
```

5. Open a pull request with a short summary, testing notes, and any follow-up ideas.

## Adding Or Updating A Skill

1. Start from `_template/` when creating a new skill.
2. Use a short, action-led, kebab-case name such as `capture` or `github-actions`.
3. Include YAML frontmatter in `SKILL.md` with:
   - `name`
   - `description`
4. Keep the skill focused on one primary job.
5. Add `references/` only when they meaningfully improve accuracy or execution.
6. Update [README.md](README.md) so the skill is discoverable.
7. If you add, remove, or rename a packaged skill, update `plugin-skills/` so the Codex plugin surface stays in sync.

## Writing Guidelines

- Prefer direct, imperative instructions over abstract advice.
- Optimize for fast execution in real repositories.
- State guardrails clearly when a skill should not activate.
- Keep examples realistic and short.
- Avoid adding supporting files unless they materially improve the skill.

## Pull Request Checklist

- The change is scoped to one clear improvement.
- User-facing docs match the current behavior.
- New or renamed skills are listed in [README.md](README.md).
- `python3 scripts/validate_repo.py` passes locally.
- Packaging manifests and `plugin-skills/` stay aligned with the current repo contents.

## Reporting Problems

- Use GitHub issues for bugs, docs gaps, and feature requests.
- Use the issue templates when they fit.
- Read [SECURITY.md](SECURITY.md) before reporting anything security-sensitive.
