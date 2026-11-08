# Documentation Rules

These rules apply to all documentation work in this repository, regardless of workflow.

## Decision escalation

Apply this rule across workflows, regardless of the active skill. Before you ask the user to choose, assess reversal cost.

- For a local, unshared change with a simple undo path, decide from the user's goal, the specification, project conventions, and available evidence.
- For an unresolved hard or unclear choice, stop and ask before you change files, data, shared state, or external systems.
- Give no more than three numbered options. State the main consequence and reversal cost for each option. Recommend an option only when evidence supports it.
- Treat a clear direct user request as the user's input when it names the action and required facts. Do not ask for redundant approval.
- Gather safe evidence when the agent lacks critical facts. Do not invent facts or bypass security, privacy, legal, or data-safety requirements.
- When you ask for missing facts about a hard or unclear choice, use up to three numbered options. The options can request source evidence, authorize a safe read-only check, or defer the change.
- Use `jev_evaluate` for meaningful choices when the tool is available. Use the same decision criteria when it is not available.
- For autonomous choices, record `Ruling: <what> — <why> — Impact if wrong: <cost>`. List up to three rejected alternatives with brief reasons. Do not label the decision “easy to reverse.” Do not invent alternatives.

## Creating skills

For new skills, add a concise root AGENTS.md rule and an independent SKILL.md by default. Keep repo-wide behavior in this file. Keep detailed workflows in the skill.

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
