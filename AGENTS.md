# Documentation Rules

These rules apply to all documentation work in this repository, regardless of workflow.

## Diataxis

Classify a document by the reader's need:

- Use tutorials for guided learning.
- Use how-to guides for goal-oriented tasks.
- Use reference for accurate technical facts.
- Use explanation for context, concepts, and rationale.

Use these locations:

- Tutorials: `docs/tutorials/`
- How-to guides: `docs/how-to/`
- Reference: `docs/reference/`
- Specifications: `docs/reference/specifications/`
- Explanation: `docs/explanation/`
- ADRs: `docs/explanation/decisions/`

Do not use workflow-specific directories for durable documents. If a requested document mixes user needs, ask before a major restructure.

## STE

Use Simplified Technical English (STE), ASD-STE100 Issue 9, for all documentation. Use another style only when the user explicitly asks for it.

Use procedural rules for instructions and descriptive rules for other text. Keep procedural sentences to 20 words. Keep descriptive sentences to 25 words. Preserve technical meaning, established terms, names, code, commands, and identifiers.

Run `ste lint --mode=flavored --format=agent --no-config` on authored Markdown when the `ste` command is available. Review each finding. Do not claim formal STE certification.

## Specifications, ADRs, and Plans

Read relevant specifications and ADRs before planning related work. Read existing documentation before you change the system. Do not rewrite a document only because its text is not STE.

Store active implementation plans in `plans/`. Every plan must include a task to update relevant specifications, ADRs, and user documentation. Update those durable documents before the work is complete. Then delete the plan. Do not archive completed plans by default.
