# ADR 0002: Reversibility-Based Decision Escalation

- Status: Accepted
- Date: 2026-11-08

## Context

Agents can ask the user to choose between options. They can also make a ruling. The cost to reverse a wrong choice can vary.

An on-demand skill alone cannot govern every workflow. Another skill can handle a task without loading it. The root `AGENTS.md` applies the rule across workflows in this repository. A separate skill tells agents how to apply the rule. Users can install it on its own.

## Decision

Use the cost and risk of reversal to decide whether an agent can choose or must ask the user.

For a local, unshared change with a simple undo path, the agent uses the user's goal, specifications, project conventions, and available evidence. For meaningful choices, the agent uses `jev_evaluate` when available. It records the choice, reason, and impact if wrong. It lists up to three rejected alternatives when real alternatives exist.

For an unresolved hard or unclear choice, the agent asks the user before it changes files, data, shared state, or external systems. The agent presents up to three numbered options. It states the consequence and reversal cost of each option. It recommends an option only when evidence supports it.

A clear, complete user request counts as the user's input. The agent does not ask for redundant approval. It asks when the request leaves a material choice unresolved, critical facts unavailable, or higher-priority rules require approval.

Use root `AGENTS.md` for the repo-wide rule. Keep detailed guidance in the independently installable `reversible-decisions` skill. Use this pair as the default when new skills need to affect work across this repository.

## Consequences

Agents can make supported choices for safe, local changes without asking for approval. Users receive numbered choices before unresolved high-impact changes.

The JEV tool is optional. Agents use the same criteria without it. This policy applies only in this repository and does not modify upstream skills or global Pi instructions.
