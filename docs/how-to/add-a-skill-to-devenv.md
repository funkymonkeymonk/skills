# Add a repository skill to a devenv environment

Use this guide to expose one skill from this repository to an agent in another project. `devenv` links the skill directory into the project when you enter its shell.

This guide uses the project-level `.agents/skills/` directory. The method works with agents that scan this Agent Skills location.

## Requirements

- Install `devenv` in the target project.
- Confirm that the target agent reads project skills from `.agents/skills/`.
- Replace `<owner>/<repo>` with this repository's GitHub owner and name.

## Add the skill

1. In the target project's `devenv.yaml`, add this repository as a non-flake input. Keep any existing inputs.

   ```yaml
   inputs:
     agent-skills:
       url: github:<owner>/<repo>
       flake: false
   ```

2. In the target project's `devenv.nix`, map the skill directory into `.agents/skills/`. Keep any existing function arguments and settings.

   ```nix
   { inputs, ... }:
   {
     files.".agents/skills/diataxis-docs".source =
       inputs.agent-skills + "/skills/diataxis-docs";
   }
   ```

   Replace `diataxis-docs` in both paths with a directory name under this repository's `skills/` directory. The directory link includes `SKILL.md` and any supporting files.

3. Enter the target project's devenv shell.

   ```sh
   devenv shell
   ```

   `devenv` creates or updates `.agents/skills/diataxis-docs` as a link to the pinned input. Commit `devenv.yaml`, `devenv.nix`, and `devenv.lock` so the team uses the same revision.

4. Confirm that the skill is available.

   ```sh
   test -f .agents/skills/diataxis-docs/SKILL.md
   ```

## Update the skill

Run `devenv update agent-skills` to select a newer input revision. Review the change to `devenv.lock`, then enter `devenv shell` again. Review skill content before you update it because a skill contains instructions for your agent.

## Notes

- Add another `files` entry for each additional skill. Each entry can use a different directory under `skills/`.
- The link points to the read-only Nix store. Edit the skill in its source repository, not through the project link.
- Check that `.agents/skills/diataxis-docs` does not already exist. `devenv` reports a conflict instead of replacing an unmanaged path.
- Do not use `imports` for a skill directory. `imports` composes devenv configuration. Use `files` to link the skill into the project. See [devenv composition](https://devenv.sh/composing-using-imports/).
- This setup exposes skills to compatible agents. It does not install agent software or enable a skill integration that scans another directory.
- `devenv` also has Claude Code-specific skill options. Use those options when you need Claude Code integration rather than a project-wide Agent Skills directory. See [devenv's Claude Code integration](https://devenv.sh/integrations/claude-code/).

## References

- [devenv inputs](https://devenv.sh/inputs/)
- [devenv composing using imports](https://devenv.sh/composing-using-imports/)
- [devenv declarative files](https://devenv.sh/creating-files/)
- [Agent Skills specification](https://agentskills.io/specification)
