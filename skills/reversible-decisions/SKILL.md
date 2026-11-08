---
name: reversible-decisions
description: Use when an agent must decide whether to ask the user before a change, choose between options, or assess reversal cost.
---

# Reversible Decisions

Use this policy in any workflow, even when another skill is active. Follow the repository's `AGENTS.md` rules.

## Check the request

Identify the user's goal, known facts, and the available options. Do not invent facts.

A clear direct request counts as user input when it names the action and supplies the required facts. Do not ask for redundant approval. Follow higher-priority safety and authorization rules.

If critical facts are absent, gather safe evidence. When critical facts are not available for a hard or unclear choice, ask the user with up to three numbered options. Offer options to send source evidence, authorize a safe read-only check, or defer the change. Do not ask an open-ended question for these choices.

## Assess reversal cost

Classify each relevant choice:

- **Easy:** The change is local, unshared, and simple to undo. It has no external effect or user-data risk.
- **Hard:** The change is destructive, irreversible, public, shared, or external. It can also risk data loss, security, privacy, legal effects, or costly recovery.
- **Unclear:** You cannot establish the reversal cost from the available facts. Treat this as hard until you gather safe evidence.

Do not ask the user to choose a low-risk local option. Select the best-supported option from the user's goal, specifications, project conventions, and available evidence. Prefer the smallest change with a clear recovery path.

## Compare meaningful options

Use `jev_evaluate` when it is available and two or more options have meaningful tradeoffs. Compare:

- Fit to the user's goal and specifications.
- Support from available evidence.
- Impact if the choice is wrong.
- Effort and risk to recover.

Do not use JEV for trivial choices. If `jev_evaluate` is unavailable, compare the same criteria directly. Do not treat a score as permission to bypass a safety rule.

## Record an autonomous choice

Use this format:

```text
Ruling: <what> — <why> — Impact if wrong: <cost>
Rejected alternatives:
1. <alternative> — <reason for rejection>
```

List no more than three alternatives. Include only real options. Omit the list when no reasonable alternative exists. Do not say that a decision is “easy to reverse.”

## Ask for unresolved hard choices

Do not act while a material, hard-to-reverse choice remains unresolved. Present no more than three numbered options. For each option, state its main consequence and reversal cost. Mark a recommendation only when the evidence supports it.

Ask the user to reply with a number. Wait for the reply before you change files, data, shared state, or external systems.

A clear, complete user request is already user input. Do not ask the user to confirm it again only because reversal is difficult. Ask only when a material choice or critical fact remains unresolved, or a higher-priority rule requires approval.
