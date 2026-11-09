# Selective Superpowers Skill Vendoring

## Status

Implementation is complete. This document records the accepted design and verified behavior.

## Problem

This repository must offer selected skills from `obra/superpowers` without importing every upstream skill. Each selected skill needs a pinned upstream revision. The repository must propose upstream changes as reviewable pull requests.

## Goals

- List every selected upstream skill explicitly.
- Pin each selected skill to an exact upstream Git commit.
- Copy only selected skill directories into this repository.
- Detect upstream changes and create one reviewable pull request per changed skill.
- Run checks weekly and on manual request.
- Let users install mirrored skills with the Vercel Skills CLI.
- Create the GitHub repository `funkymonkeymonk/skills` as a private repository.
- Include the existing `README.md` and `docs/how-to/` changes in this repository.

## Design

### Source manifest and vendored files

Store the upstream selection and pins in `upstreams.json`. Each entry identifies the upstream repository, skill name, source path, license path, and exact commit SHA.

Store vendored skills under `skills/<name>/`. Store each matching license at `licenses/upstream/<name>-LICENSE`. The destination paths derive from the skill name. The manifest is an allowlist. The sync task must not add skills that are absent from the manifest.

Start with an empty upstream selection because the user has not named any skills. This prevents an unrequested skill from entering the repository. Add a skill only when the user adds its manifest entry.

Keep the upstream MIT license and attribution with the vendored content. Do not modify upstream skill text during synchronization.

### Synchronization and version checks

Use `scripts/vendor_skills.py sync` to read the manifest and synchronize its entries. Use each entry's exact commit SHA. Reject invalid paths, duplicate skill names, missing source directories, and symbolic links. Do not execute upstream files.

Use `scripts/vendor_skills.py update` to check the newest upstream commit that affects each selected skill path or license file. If either path changed after its pin, prepare an update with the new content and exact commit SHA. Do not change the default branch during the check.

Create one pull request per changed skill. Include the old and new commit SHAs and the upstream skill path in each pull request. Do not merge pull requests automatically. Merge a pull request to apply an update. Close it to reject the current update.

Do not create another pull request for a skill while its update pull request remains open. Do not recreate a closed pull request for the same skill and revision. Create a new pull request when a later upstream revision changes that skill.

### Devenv tasks, GitHub automation, and installation

Define `skills:vendor` to synchronize exact pins. Define `upstreams:check` to check upstream changes and open review pull requests. Define `check:lint` for repository checks. Commit `devenv.lock` to pin environment inputs.

Keep the Python script as the shared implementation. Keep the GitHub workflow calling that script directly. Do not add Nix setup to GitHub Actions.

Ruling: Use devenv tasks for local commands and keep GitHub Actions calling Python — this avoids Nix setup in CI. Impact if wrong: local and scheduled checks use different entry points.

Rejected alternatives:

1. Run the devenv task in GitHub Actions — this adds Nix setup to the workflow.

Run the update check every Monday at 09:17 UTC and through a manual workflow trigger. Give the workflow only `contents: write` and `pull-requests: write` permissions.

Keep the workflow limited to manifest entries. Treat upstream content as data and do not run scripts from upstream skills.

Install an individual mirrored skill with the Vercel Skills CLI, for example:

```bash
npx skills add funkymonkeymonk/skills --skill <name> --agent pi
```

The user must have read access to the private repository. Use an authenticated Git or GitHub CLI path supported by the Skills CLI.

### Failure behavior

Stop a skill update when the manifest is invalid, GitHub access fails, an upstream path does not exist, or a copy would escape its destination. Report the skill and error. Do not create a pull request for that skill.

A failure for one skill must not discard valid updates for other skills. Report each skill result separately.

### Tests

Use local fixture Git repositories to test manifest validation, exact-commit synchronization, skill and license change detection, per-skill update proposals, idempotency, and path safety. Tests must not require network access or GitHub credentials.

Check the GitHub workflow permissions and triggers with automated structural tests. After repository creation, test installation from the private repository with the Skills CLI and the user's authenticated `gh` setup.

## Decisions

Ruling: Use exact Git commit pins and vendored files — this supports selected skills, visible diffs, and independent review. Impact if wrong: the sync tool needs maintenance when upstream changes its layout.

Rejected alternatives:

1. Install directly from upstream with the Skills CLI — this lacks repository-owned update PRs for selected skills.
2. Use Git submodules — this adds submodule handling to installation and skill discovery.

Ruling: Create one pull request per skill — this lets the user accept or reject each update independently. Impact if wrong: a weekly run can create several pull requests.

Rejected alternatives:

1. Combine all updates in one pull request — this makes independent acceptance require manual edits.

Ruling: Start with an empty upstream list — the user has not named skills, so this blocks unrequested imports. Impact if wrong: no upstream skills are available until the user adds entries.

Rejected alternatives:

1. Select common Superpowers skills by default — this would invent the user's desired selection.

Ruling: Run the update check weekly and on manual request — this follows the user's instruction. Impact if wrong: scheduled checks can create unwanted review pull requests, which the user can close.

Rejected alternatives:

1. Run checks only on manual request — this would require the user to remember each check.

## Acceptance criteria

- `upstreams.json` pins each selected skill to an exact commit SHA and records its license path.
- Synchronization copies only allowlisted skill paths and does not modify upstream content.
- The weekly and manual update workflow creates separate, review-only pull requests for changed skills.
- The update process does not create duplicate pull requests for a skill and revision, and it does not reopen a rejected revision.
- The updater continues with other skills when one skill fails.
- Tests cover manifest validation, pinning, change detection, PR proposal behavior, and path safety without network access.
- The Vercel Skills CLI can install a selected skill from the private repository.
- The repository preserves the upstream license and attribution.
- The existing `README.md` and `docs/how-to/` changes remain included.

## Implementation results

- All 21 Python tests passed.
- Both existing structural Bash tests passed.
- STE flavored lint returned `ste: clean.`
- `devenv tasks run skills:vendor`, `devenv tasks run upstreams:check`, and `devenv tasks run check:lint` passed.
- GitHub created `funkymonkeymonk/skills` as a private repository.
- The Skills CLI installed only `diataxis-docs` from the private repository in a temporary project.
- Manual workflow run [42513336792](https://github.com/funkymonkeymonk/skills/actions/runs/42513336792) completed successfully.
- The upstream allowlist remains empty because the user has not selected skills. Fixture tests verified update pull request behavior. The workflow created no live upstream update pull requests.
