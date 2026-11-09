# ADR 0003: Selective Superpowers Skill Vendoring

- Status: Accepted
- Date: 2026-11-08

## Context

This repository stores personal Agent Skills. The owner wants selected skills from `obra/superpowers`, not the full upstream set.

Direct installation does not keep a pinned source copy or create reviewable upstream update pull requests. A private repository must keep its selection explicit.

## Decision

Create `funkymonkeymonk/skills` as a private GitHub repository. Keep an explicit allowlist in `upstreams.json`. Pin each selected skill to an exact Git commit SHA.

Copy only selected skill directories into `skills/`. Preserve the matching upstream license in `licenses/upstream/`. Do not execute upstream files or modify upstream content during synchronization.

Use `scripts/vendor_skills.py` to synchronize exact pins and open update pull requests. Expose local synchronization and update checks through devenv tasks. Keep GitHub Actions calling the Python script directly. Commit `devenv.lock` to pin environment inputs.

Run the check weekly and on manual request. Create one review-only pull request per changed skill. Do not merge pull requests automatically.

Use the Vercel Skills CLI to install selected skills from this repository. Keep the initial upstream allowlist empty until the owner selects skills.

## Consequences

The owner can review and accept or reject each skill update. The manifest shows which upstream revision each vendored skill uses. The private repository requires authenticated access for installation and pull request updates.

The owner must add a manifest entry to include a skill. The workflow does not add new upstream skills automatically.

## Rejected alternatives

1. Install skills directly from upstream — this cannot create repository-owned update pull requests.
2. Use Git submodules — this adds submodule handling to skill installation and discovery.
