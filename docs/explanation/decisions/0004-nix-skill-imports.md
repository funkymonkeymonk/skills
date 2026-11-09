# ADR 0004: Nix Skills in the Personal Skills Repository

- Status: Accepted
- Date: 2026-11-09

## Context

The `funkymonkeymonk/nix` repository manages skills through a Nix manifest. This repository makes each skill available for individual installation with the Skills CLI.

The owner asked to copy four distinct skills into this repository. The Nix manifest must continue to deploy its existing copies.

## Decision

Copy these skill directories and their supporting files from Nix commit `7edb8145c8935436b600a36a05a93d2405979b93` into `skills/`:

- `consumer-decision-guides`
- `creating-user-manual`
- `devenv`
- `ste-implementation-plans`

Keep `funkymonkeymonk/nix` unchanged. Its Nix manifest still deploys its copies. This repository does not track updates from `nix`. Review and copy later changes manually.

Keep `ste-implementation-plans` separate from `writing-plans`. Use the general skill for implementation plans. Use the STE skill when the user explicitly requests an STE plan. This keeps the specialized skill independently installable.

Ruling: Keep the two planning skills separate — one writes general plans and one targets explicit STE requests. Impact if wrong: users receive overlapping guidance when they install both.

Rejected alternatives:

1. Merge the STE guidance into `writing-plans` — users could not install the STE workflow by itself.
2. Delete the skills from `nix` — this would remove skills from its active Nix manifest.

## Consequences

The personal skills repository can install each copied skill by itself. The Nix repository continues to use its existing skill directories.

Future changes in `nix` do not update these copies automatically. Review and copy changes when needed.
