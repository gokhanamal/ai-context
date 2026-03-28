# Skills

A collection of custom Claude Code skills for extending Claude's capabilities.

## Repository Structure

```
skills/
├── _template/              # Template for creating new skills
│   ├── SKILL.md            # Core skill definition (required)
│   ├── agents/             # Sub-agent definitions (optional)
│   └── references/         # Supporting docs & examples (optional)
├── <skill-name>/           # Each skill is a kebab-case directory
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── README.md
├── LICENSE
└── .gitignore
```

## Installation

Add a skill to Claude Code by placing its directory under your Claude Code skills path, or by referencing this repository in your configuration.

## Adding a New Skill

1. Copy the `_template/` directory and rename it using kebab-case (e.g. `my-new-skill/`)
2. Edit `SKILL.md` with your skill definition
3. Optionally add agents in `agents/` and reference materials in `references/`
4. Add an entry to the skills table below

## Skills

| Skill | Description |
|-------|-------------|
| [github-actions](github-actions/) | Create, edit, debug, and optimize GitHub Actions workflows and custom actions |

## Contributing

Contributions are welcome! When adding a skill, please ensure it has:

- A clear, single purpose
- Comprehensive documentation in `SKILL.md`
- Consistent structure following the template
- Supporting reference materials where helpful

## License

[MIT](LICENSE)
