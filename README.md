[![Validate](https://github.com/gokhanamal/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/gokhanamal/skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# Skills

Reusable, inspectable skills for AI coding agents.

This repository packages small, task-specific workflows that work well in both [Claude Code](https://code.claude.com) and [OpenAI Codex](https://openai.com/index/introducing-codex/). The goal is to keep each skill easy to install, easy to audit, and easy to extend.

## Why This Repo Exists

- Cross-platform packaging for Claude Code and Codex
- Human-readable Markdown skills with optional references
- Practical workflows instead of abstract prompt collections
- Low-friction contribution path for new skills and improvements

## Included Skills

| Skill | What it helps with |
|-------|---------------------|
| [github-actions](github-actions/) | Create, review, debug, and harden GitHub Actions workflows and custom actions |
| [capture](capture/) | Decide whether reusable knowledge belongs in a skill, lesson, solution doc, or nowhere at all |

## Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| Claude Code | Yes | Includes `.claude-plugin/` manifest and marketplace catalog |
| OpenAI Codex | Yes | Includes `.codex-plugin/` manifest and local marketplace catalog |
| Manual install | Yes | Copy any skill folder directly into your agent's skills directory |

## Quick Start

### Claude Code

Install directly from GitHub:

```bash
claude plugin install --source github gokhanamal/skills
```

Add this repository as a marketplace:

```text
/plugin marketplace add gokhanamal/skills
/plugin install gokhanamal-skills@gokhanamal-plugins
```

Test the marketplace locally from the repo root:

```text
/plugin marketplace add .
/plugin install gokhanamal-skills@gokhanamal-plugins
```

Load the plugin directory directly from the repo root:

```bash
claude --plugin-dir .
```

### OpenAI Codex

Pick the workflow that fits how you like to install skills:

1. Copy one or more skill directories into `$HOME/.agents/skills/`.
2. Use the repo-local marketplace manifest in `.agents/plugins/marketplace.json`.
3. Use the packaged Codex plugin manifest in `.codex-plugin/plugin.json`.

### Manual Install

Copy any skill directory, such as `github-actions/` or `capture/`, into your agent's skills folder.

## Creating A New Skill

1. Copy `_template/` to a new kebab-case directory such as `my-new-skill/`.
2. Update `SKILL.md` frontmatter with the final `name` and `description`.
3. Add `references/` or `agents/` content only when it genuinely helps the skill.
4. Add the new skill to the table in this README.
5. If the skill is packaged for Codex, keep `plugin-skills/` aligned with the skill directory names.
6. Run the repository validation script before opening a pull request:

```bash
python3 scripts/validate_repo.py
```

## Repository Layout

```text
skills/
├── .agents/plugins/        # Codex marketplace catalog for local testing
├── .claude-plugin/         # Claude Code plugin manifest and marketplace catalog
├── .codex-plugin/          # Codex plugin manifest
├── .github/                # Issue templates, PR template, and CI validation
├── _template/              # Starter template for new skills
├── plugin-skills/          # Packaged skill aliases used by the Codex plugin
├── <skill-name>/           # Skill directory with required SKILL.md
│   ├── SKILL.md
│   ├── agents/             # Optional
│   └── references/         # Optional
├── scripts/                # Local validation helpers
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── README.md
└── LICENSE
```

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow, authoring checklist, and validation steps. By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Please review [SECURITY.md](SECURITY.md) before reporting a vulnerability publicly.

## License

[MIT](LICENSE)
