# Reversibility-Based Decision Policy

## Status

This document records the approved design and completed implementation.

## Problem

An agent must sometimes decide whether to ask the user or make a ruling. The subagent-driven workflow tells agents to make rulings for many open decisions. A wrong decision can require different amounts of work to reverse.

This repository needs a clear rule. Agents must decide when they can safely reverse a change. They must ask when a hard-to-reverse choice remains unresolved. This rule must apply across workflows in this repository.

## Goals

- Use the cost of reversal to decide when to ask the user.
- Make low-risk, reversible decisions without asking for approval.
- Ask when a hard-to-reverse or uncertain choice remains unresolved.
- Treat a clear, complete user request as the user's input. Do not ask for redundant approval.
- Record the decision, reason, and impact if the decision is wrong.
- Show up to three rejected alternatives for review.
- Give the user a clear numbered choice when an agent must ask.
- Use `jev_evaluate` for meaningful choices when this tool is available.
- Make a paired `AGENTS.md` rule and skill the default for new skills in this repository.
- Keep the rule local to this repository. Do not change global Pi instructions or upstream skills.

## Design

### Repo-wide policy

Update the root `AGENTS.md` with a short decision rule. The rule applies across workflows in this repository, even when another skill handles the task.

The root `AGENTS.md` will also define the default for new skills. Create each skill as an independent Agent Skill. Add a concise root `AGENTS.md` rule for behavior that must apply across workflows. Put detailed workflow instructions in the skill. Do not rely on an on-demand skill alone for a repo-wide rule.

### Decision process

Before an agent makes a choice, it must:

1. Identify the user's goal, the known facts, and the available options.
2. Check whether missing facts make every option a guess. Do not invent facts.
3. Estimate the effort and impact to reverse each option.
4. Classify the safest applicable option as easy, hard, or unclear to reverse.

An option is easy to reverse when it is local, unshared, and simple to undo. It must not affect user data, an external system, a public service, or another person.

An option is hard to reverse when it is destructive, irreversible, public, shared, or external. It is also hard to reverse when it can cause data loss, security or privacy problems, legal effects, or costly recovery work.

When the agent cannot establish the reversal cost, it must classify the option as unclear. It must treat an unclear option as hard to reverse until it gathers safe evidence.

A clear direct user request counts as the user's input when it names the action and supplies the required facts. Do not ask for approval again only because the action is hard to reverse. Follow higher-priority safety and authorization rules. Ask when a material choice remains unresolved or the agent lacks critical facts.

For an easy-to-reverse choice, the agent must decide without asking the user. It must use the user's goal, the specification, project conventions, and available evidence. It must choose the smallest option that meets the requirements and has a clear rollback path.

Use `jev_evaluate` when it is available and the agent must compare two or more meaningful options. Evaluate fit to the user's goal, evidence, impact if wrong, and recovery effort. Do not use the tool for trivial choices. If the tool is not available, apply the same criteria directly.

Record an autonomous choice in this form:

```text
Ruling: <choice> — <reason> — Impact if wrong: <cost>
Rejected alternatives:
1. <alternative> — <reason for rejection>
```

List no more than three rejected alternatives. Do not label a decision “easy to reverse.” Do not invent alternatives to fill the list. Omit the list when no reasonable alternative exists.

For an unresolved hard or unclear choice, the agent must stop before it changes files, data, shared state, or external systems. It must give the user no more than three numbered options. Each option must state its main consequence and reversal cost. The agent can identify a recommended option only when the available evidence supports it. Ask the user to choose by number. Do not proceed until the user replies.

### Skill package

Create `skills/reversible-decisions/SKILL.md` with valid Agent Skills metadata. Its description must state when to use the skill. It must cover decision points across workflows, not only subagent-driven development.

Keep the skill concise. Use it for the detailed classification rubric, `jev_evaluate` guidance, ruling format, and numbered questions. Do not modify or copy upstream Superpowers skills.

### Tests

Use the writing-skills method for skill testing. Record a no-skill baseline, then apply the skill to the same scenarios in fresh contexts.

The scenarios must test these results:

- For an easy local choice, the agent decides without asking. It records a ruling and no more than three rejected alternatives.
- For an unresolved destructive or external choice, the agent asks with numbered options and takes no action.
- For a clear direct request with all required facts, the agent does not ask for redundant approval.
- For a hard request with missing critical facts, the agent asks for those facts before it acts.
- For unclear reversal costs, the agent asks or gathers safe evidence before deciding.
- When `jev_evaluate` is available, the agent uses it for a meaningful choice. Without it, the agent uses the same rubric.
- The root `AGENTS.md` rule applies when a different skill handles the task.

The structural test must check the skill metadata and the repo policy. Use STE lint on authored documentation. Do not lint prompt fixtures that ask for a non-STE output.

## Out of scope

- Do not modify upstream Superpowers skills.
- Do not change global Pi instructions.
- Do not apply this repo's `AGENTS.md` policy to other repositories.
- Do not ask the user to choose between low-risk local edits.

## Implementation results

The no-skill baseline asked for a preference in the easy case. It suggested a destructive migration after a backup check. It also asked for redundant approval on a complete direct request.

With the skill, the agent chose the local option and recorded a ruling. It asked for numbered choices before the unresolved migration. It accepted the direct request without a second approval. It asked for numbered information options about the unclear billing setting and changed nothing.

JEV selected the hybrid test approach with confidence `1`. The fallback scenario used the same decision criteria without JEV.

The structural test passed. STE flavored lint returned `ste: clean.` The Vercel Skills CLI installed only `reversible-decisions` in a temporary Pi project. Git ignored `plans/`, the local PDF, and harness artifacts. The PDF is not tracked.

## Acceptance criteria

- The root `AGENTS.md` contains a short reversibility policy for all workflows in this repository.
- The root `AGENTS.md` defines the paired `AGENTS.md` plus skill approach as the default for new skills.
- `skills/reversible-decisions/SKILL.md` is independently installable and follows the Agent Skills specification.
- The skill uses `jev_evaluate` when available for meaningful choices and has a rubric fallback.
- Easy-to-reverse choices do not prompt the user. Their rulings state what, why, impact if wrong, and up to three rejected alternatives.
- Unresolved hard or unclear choices stop for a numbered user choice before the agent acts.
- A clear direct request counts as user input. The agent does not ask for redundant approval when it has the required facts and no higher-priority rule requires it.
- Tests cover easy, hard, and unclear reversal cases.
- The design spec, skill, and ADR use the approved Diataxis locations and STE by default.
