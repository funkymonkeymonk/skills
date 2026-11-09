# Vendor a Superpowers skill

Use this guide to add one selected skill from `obra/superpowers` to this repository. The manifest pins each skill to an exact Git commit.

## Requirements

- Read access to `obra/superpowers`.
- Devenv.
- A GitHub CLI login with access to `funkymonkeymonk/skills` for update checks.

Devenv supplies Python 3, Git, and the GitHub CLI in its task environment.

## Select and pin a skill

1. Clone the upstream repository.

   ```sh
   git clone https://github.com/obra/superpowers.git /tmp/superpowers
   ```

2. Review the skill directory and its supporting files. Confirm that you want this skill in the private repository.

3. Find the latest commit that changed the skill directory.

   ```sh
   git -C /tmp/superpowers log -1 --format=%H HEAD -- skills/<name>
   ```

4. Add an entry to `upstreams.json`. Replace `<name>` and `<commit-sha>` with the selected values. Use the full commit SHA.

   ```json
   {
     "version": 1,
     "skills": [
       {
         "name": "<name>",
         "repository": "https://github.com/obra/superpowers.git",
         "path": "skills/<name>",
         "license_path": "LICENSE",
         "ref": "<commit-sha>"
       }
     ]
   }
   ```

   Keep every wanted skill entry. Add one object for each new selected skill.

5. Synchronize the pinned files.

   ```sh
   devenv tasks run skills:vendor
   ```

6. Review the diff. Confirm that it contains only the selected skill and its upstream license.

7. Commit `upstreams.json`, `skills/<name>/`, and `licenses/upstream/<name>-LICENSE`.

## Remove a skill

1. Remove its entry from `upstreams.json` to stop update checks.
2. Delete `skills/<name>/` and `licenses/upstream/<name>-LICENSE` to remove the vendored copy.
3. Commit the manifest and file changes.

## Check for updates

GitHub checks upstream skills every week and on manual request. Each changed skill gets its own review pull request. The workflow does not merge pull requests.

To run the check locally, authenticate with `gh` and run:

```sh
devenv tasks run upstreams:check
```

Review each pull request before you merge it. Close a pull request to reject its current revision. The workflow does not reopen a rejected revision. It can propose a later upstream revision.

## Install a selected skill

Use the Vercel Skills CLI to install one skill from this private repository:

```sh
npx skills add funkymonkeymonk/skills --skill <name> --agent pi --global
```

The GitHub account used by the CLI must have read access to the private repository.
