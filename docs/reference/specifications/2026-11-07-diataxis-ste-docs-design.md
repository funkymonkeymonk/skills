# Diataxis and STE Technical Writing Design

## Status

Accepted. ADR 0005 records the skill boundaries.

## Problem

This repository needs independently installable skills for documentation structure, STE language guidance, and implementation-plan workflow.

Repository rules apply to documentation regardless of the active skill. The Superpowers `writing-plans` skill also needs to retain its plan format and execution handoff.

## Goals

- Use Diataxis to select documentation purpose and structure.
- Apply ASD-STE100 Issue 9 language guidance to technical documents by default.
- Keep implementation-plan workflow compatible with Superpowers execution skills.
- Keep each skill independently installable.
- Keep specifications and ADRs as durable records.
- Keep implementation plans temporary and remove them when work is complete.
- Allow an explicit user request for another style.

## Skill boundaries

### `diataxis-docs`

Use this skill to select structure for reader-facing documentation based on reader need. Preserve established ADR, specification, and implementation-plan formats.

- Use tutorials for guided learning.
- Use how-to guides for goal-oriented tasks.
- Use reference for accurate, complete technical facts.
- Use explanation for context, concepts, and rationale.

Use this skill to guide reader-facing content organization and repository locations. For implementation-plan structure and workflow, use `writing-plans`. This skill does not define STE language rules or lint commands.

### `ste-technical-writing`

Use this skill for STE language guidance on technical documents. This includes ADRs, specifications, implementation plans, tutorials, how-to guides, reference, and explanation.

Preserve technical meaning, approved project terms, names, code, commands, and identifiers. Treat flavored lint findings as advisory. Do not claim formal STE certification. Do not rewrite existing documents only because they do not use STE.

This skill governs language. It does not define document structure or workflow. An explicit user request for another style overrides the STE default.

### `writing-plans`

Use the vendored Superpowers skill for implementation-plan process and structure. Keep its plan format, task steps, self-review, and execution handoff intact. Apply `ste-technical-writing` to plan prose. Do not edit the vendored skill as part of this design.

## Repository policy

The root `AGENTS.md` applies documentation rules to work in this repository, regardless of the active skill. It does not change global Pi instructions or apply to other repositories.

Read relevant specifications and ADRs before related work. When a system changes, update durable documentation to describe the implemented system. Do not rewrite existing documentation only because it does not use STE.

## Locations and lifecycle

Use these locations in this repository:

- Tutorials: `docs/tutorials/`
- How-to guides: `docs/how-to/`
- Reference: `docs/reference/`
- Specifications: `docs/reference/specifications/`
- Explanation: `docs/explanation/`
- ADRs: `docs/explanation/decisions/`

Store active implementation plans in `plans/`. Do not classify a plan as a user-facing how-to guide. Every plan must include a task to update relevant specifications, ADRs, and user documentation. Delete the plan after the work and documentation updates are complete.

## STE checks

When `ste` is available, check authored Markdown with:

```bash
ste lint --mode=flavored --format=agent --no-config path/to/file.md
```

Review every finding. Keep changes that preserve meaning and improve clarity. Use dictionary checks only when a local Issue 9 dictionary index is available. Do not include the ASD-STE100 PDF or a generated dictionary index in a skill package.

## Distribution

Keep each skill in its own directory under `skills/`. Users can install each skill by name with the Vercel Skills CLI.

This repository does not update the Nix repository's separate `ste-implementation-plans` copy. Do not change that repository as part of this design.

## Acceptance criteria

- `diataxis-docs` focuses on document purpose and structure.
- `ste-technical-writing` covers technical-document language and advisory STE lint.
- `writing-plans` remains unchanged and defines the plan workflow and format.
- A plan can use both `writing-plans` and `ste-technical-writing` without conflicting instructions.
- ADRs and other technical documents can use STE without adopting the implementation-plan format.
- The Nix repository remains unchanged.
