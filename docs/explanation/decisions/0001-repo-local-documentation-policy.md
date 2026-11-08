# ADR 0001: Repo-Local Documentation Policy

- Status: Accepted
- Date: 2026-11-07

## Context

This repository stores skills for Pi and other agents. The Vercel Skills CLI must install each skill on its own.

Different workflows can write or read specifications and ADRs. Rules inside one skill may not apply when another skill handles the task. The documentation policy must apply across workflows in this repository.

Global Pi instructions affect all projects. This policy must apply only in this repository.

## Decision

Keep detailed Diataxis and STE writing guidance in one portable Agent Skill named `diataxis-docs`.

Use the root `AGENTS.md` for short documentation rules that apply to all workflows in this repository. Store specifications and ADRs in the approved Diataxis locations. Keep active plans in `plans/`, ignore them, and delete them after the work is complete.

Require every implementation plan to update the relevant specifications, ADRs, and user documentation. Keep those documents as the durable record of requirements, decisions, and behavior.

Do not modify global Pi instructions or upstream skills. Do not apply this policy to other repositories.

## Consequences

Each skill remains independently installable with the Vercel Skills CLI. Agents can follow one repository policy even when they use different workflows.

The Git history keeps the durable documentation, not completed plans. Other repositories need their own documentation policy.
