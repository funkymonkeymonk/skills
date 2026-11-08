# Personal Agent Skills

This repository stores skills for coding agents. Users can install each skill by itself.

Each skill has its own directory under `skills/` and a `SKILL.md` file. Use the Vercel Skills CLI to install one skill:

```bash
npx skills add <owner>/<repo> --skill diataxis-docs --agent pi --global
```

Replace `<owner>/<repo>` with this repository's GitHub owner and name. Replace `diataxis-docs` with the skill name that you want to install.

The `--global` option installs the skill for Pi across projects. Vercel's standard Pi target is `~/.agents/skills/`.

To add a skill, create a separate directory under `skills/`. Give the directory and the skill the same name. Add a `SKILL.md` file with valid Agent Skills frontmatter. Then install the skill by name with the CLI.

The root `AGENTS.md` applies documentation rules to work in this repository. It does not change your global Pi instructions or other repositories.
