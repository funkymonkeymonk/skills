# Personal Agent Skills

This repository stores skills for coding agents. Users can install each skill by itself.

Each skill has its own directory under `skills/` and a `SKILL.md` file. Use the Vercel Skills CLI to install one skill:

```bash
npx skills add <owner>/<repo> --skill diataxis-docs --agent pi --global
```

Replace `<owner>/<repo>` with this repository's GitHub owner and name. Replace `diataxis-docs` with the skill name that you want to install.

The `--global` option installs the skill for Pi across projects. Vercel's standard Pi target is `~/.agents/skills/`.

To expose a skill through another project's devenv environment, see [Add a repository skill to a devenv environment](docs/how-to/add-a-skill-to-devenv.md).

To add a skill, create a separate directory under `skills/`. Give the directory and the skill the same name. Add a `SKILL.md` file with valid Agent Skills frontmatter. Then install the skill by name with the CLI.

The root `AGENTS.md` applies documentation rules to work in this repository. It does not change your global Pi instructions or other repositories.

## Additional personal skills

This repository includes three skills from `funkymonkeymonk/nix`. Its Nix manifest still deploys its own copies.

- `consumer-decision-guides` — research and write evidence-based buying guides.
- `creating-user-manual` — create personal working-style documents.
- `devenv` — configure and use devenv environments.

## Documentation and planning skills

- `diataxis-docs` — select documentation structure by reader need.
- `ste-technical-writing` — apply STE language guidance to technical documents.
- `writing-plans` — create implementation plans with the Superpowers workflow and structure.

For an implementation plan, use `writing-plans` for the process and `ste-technical-writing` for language. Use `diataxis-docs` when a document needs a Diataxis structure. The root `AGENTS.md` sets this repository's STE policy.

The Nix repository still deploys its own `ste-implementation-plans` copy. This repository does not update that copy automatically.

## Selected Superpowers skills

The `upstreams.json` file pins all 15 current skills from `obra/superpowers` to exact Git commits. The update workflow does not add new upstream skills automatically. To stop updates for a skill, remove its manifest entry. To remove its vendored files, also delete its directory and license file.

See [Vendor a Superpowers skill](docs/how-to/vendor-a-superpowers-skill.md) to add a skill, synchronize its pinned files, and install it with the Skills CLI. Run `devenv tasks run skills:vendor` to synchronize pins. Run `devenv tasks run upstreams:check` to check upstream changes locally. GitHub also checks selected skills weekly and on manual request. It opens one review pull request per changed skill. It does not merge pull requests.
