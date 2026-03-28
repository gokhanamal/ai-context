# Skills

A collection of custom skills for AI coding agents. Works with any platform that supports the skills format, including [Claude Code](https://code.claude.com) and [OpenAI Codex](https://openai.com/index/introducing-codex/).

## Installation

### Claude Code

```bash
claude plugin install --source github gokhanamal/skills
```

Or test locally:

```bash
claude --plugin-dir ./skills
```

### OpenAI Codex

Place the skill directories under your Codex skills path (`$HOME/.agents/skills/`), or reference via a local `marketplace.json`.

### Manual

Copy any skill directory (e.g. `github-actions/`) into your agent's skills folder.

## Repository Structure

```
skills/
├── .claude-plugin/         # Claude Code plugin manifest
│   └── plugin.json
├── .codex-plugin/          # OpenAI Codex plugin manifest
│   └── plugin.json
├── _template/              # Template for creating new skills
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── <skill-name>/           # Each skill is a kebab-case directory
│   ├── SKILL.md            # Core skill definition (required)
│   ├── agents/             # Sub-agent definitions (optional)
│   └── references/         # Supporting docs & examples (optional)
├── README.md
├── LICENSE
└── .gitignore
```

## Skills

| Skill | Description |
|-------|-------------|
| [github-actions](github-actions/) | Create, edit, debug, and optimize GitHub Actions workflows and custom actions |
| [capture](capture/) | Recommend whether reusable knowledge should update an existing skill, create a new skill, add to lessons, add to solution docs, or be ignored, then apply approved updates safely |

## Adding a New Skill

1. Copy the `_template/` directory and rename it using kebab-case (e.g. `my-new-skill/`)
2. Edit `SKILL.md` with your skill definition (include YAML frontmatter with `name` and `description`)
3. Optionally add agents in `agents/` and reference materials in `references/`
4. Add an entry to the skills table above

## Contributing

Contributions are welcome! When adding a skill, please ensure it has:

- A clear, single purpose
- Comprehensive documentation in `SKILL.md`
- Consistent structure following the template
- Supporting reference materials where helpful

## License

[MIT](LICENSE)
