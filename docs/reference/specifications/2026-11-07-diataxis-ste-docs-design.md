# Diataxis and STE Documentation Skills

## Status

Implementation is complete. This document records the accepted design and final validation results.

## Problem

This repository needs independently installable Agent Skills. Its documentation must use the Diataxis framework and Simplified Technical English (STE) by default.

Superpowers and other skills can write or read specifications, ADRs, and plans. The same documentation rules apply in this repository, regardless of which skill writes the files.

## Goals

- Create a Vercel-compatible skill for documentation work.
- Use Diataxis to select the purpose and structure of each document.
- Use ASD-STE100 Issue 9 as the default language standard.
- Apply repository documentation rules to all skills used in this repository.
- Keep specifications and ADRs as durable records.
- Keep implementation plans temporary and remove them after the work is complete.
- Let users opt out of STE when they explicitly request it.

## Design

### Skill package

Create `skills/diataxis-docs/SKILL.md` with valid Agent Skills metadata. Keep the skill focused and concise. Include detailed guidance only when it helps the agent create or review documentation.

The skill supports all documentation work. This includes specifications, ADRs, plans, tutorials, how-to guides, reference, and explanation. It does not change the workflow or content structure of upstream skills.

### Repository policy

Create a root `AGENTS.md` for this repository. It applies the documentation rules to work done here, regardless of the skill in use. It does not change global Pi instructions or apply to other repositories.

Agents must read relevant specifications and ADRs before they plan or change related work. When they update a system, they must update the durable documentation so it describes the implemented system. Do not rewrite a document only because its existing text is not STE.

### Diataxis structure and locations

Select document structure by the reader's need:

- Use tutorials for guided learning.
- Use how-to guides for goal-oriented tasks.
- Use reference for accurate, complete technical facts.
- Use explanation for context, concepts, and rationale.

Use these locations in this repository:

- Tutorials: `docs/tutorials/`
- How-to guides: `docs/how-to/`
- Reference: `docs/reference/`
- Explanation: `docs/explanation/`
- Specifications: `docs/reference/specifications/`
- ADRs: `docs/explanation/decisions/`

Do not use workflow-specific directories for durable documents. Follow an existing repository convention when it is more specific. Classify content by its purpose, not only by its file name. Split content only when that improves its use.

### Plan lifecycle

Store active implementation plans in `plans/`. Add `plans/` to `.gitignore`. Do not classify an implementation plan as a user-facing how-to guide.

Every plan must include a task to update the relevant specifications, ADRs, and user documentation. The updated documents are the durable record of requirements, decisions, and behavior. After the work and documentation updates are complete, delete the plan. Do not archive plans by default.

### STE writing and checks

Apply STE to documentation by default. Use STE unless the user explicitly asks for another style. Apply the correct guidance for procedural or descriptive text. Use the Issue 9 limits of 20 words for procedural sentences and 25 words for descriptive sentences.

Preserve technical meaning, approved project terms, names, code, commands, and identifiers. Do not change a term only to improve a lint score. Do not claim formal STE certification.

Use the installed `ste` command to check authored documentation when it is available. Run flavored lint without repository configuration. Treat findings as advisory and review each finding for meaning and accuracy. Use dictionary checks only when a local Issue 9 dictionary index is available.

Do not include the ASD-STE100 PDF or a generated dictionary index in a skill package. Keep the supplied PDF local and out of Git.

### Distribution

Keep each skill in its own directory under `skills/`. A user must be able to install one skill without installing the others. Document the Vercel Skills CLI command for individual installation to Pi's standard global target.

## Implementation status

Validation passed:

- The structural test passed.
- STE flavored lint returned `ste: clean.`
- The Vercel Skills CLI installed only `diataxis-docs` in a temporary Pi project.
- Git reports `plans/`, the local Issue 9 PDF, and `.pi-subagents/` as ignored.
- The no-skill baseline combined four reader needs in one document. It also invented installation instructions, a `--help` option, and design rationale. The flavored linter found two issues: a nominalization and passive voice.
- The pressure test identified all four needs and asked before splitting the requested document. It listed the known facts, asked for missing details, and invented no behavior.
- The explicit opt-out test used a casual tone and asked for the missing product details.

## Acceptance criteria

- The new skill passes Agent Skills metadata validation.
- The Vercel Skills CLI can discover and install `diataxis-docs` by name.
- The root `AGENTS.md` defines the approved document locations and plan lifecycle.
- Git ignores `plans/` and the local ASD-STE100 PDF.
- The skill applies Diataxis structure and STE language by default.
- Each plan includes documentation updates. Agents delete the plan after they complete the work.
- This documentation design does not modify upstream Superpowers files. The separate vendoring policy allows explicit, unmodified skill copies in this repository. See [Selective Superpowers Skill Vendoring](2026-11-08-superpowers-skill-vendoring-design.md).
