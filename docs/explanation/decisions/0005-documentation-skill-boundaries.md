# ADR 0005: Separate Documentation Skill Responsibilities

- Status: Accepted
- Date: 2026-11-09

## Context

`diataxis-docs` combines document structure and STE language rules. The Superpowers `writing-plans` skill defines implementation-plan structure and workflow. ADRs, specifications, and guides also benefit from STE language guidance.

These concerns need clear boundaries. Users must be able to install each skill by itself. The Nix repository also keeps its own copy of `ste-implementation-plans`.

## Decision

Give each skill one responsibility:

- `diataxis-docs` selects documentation structure by reader need. It does not define STE rules.
- `ste-technical-writing` sets STE language rules for technical documents, including ADRs, specifications, plans, tutorials, guides, and reference.
- `writing-plans` defines the implementation-plan workflow and structure. Do not modify this vendored upstream skill.

Use `writing-plans` for implementation-plan process and `ste-technical-writing` for plan language. Use the relevant documentation skill for other documents. An explicit user style request overrides the STE default.

Rename this repository's `ste-implementation-plans` skill to `ste-technical-writing`. Keep the Nix repository unchanged. Its copy does not update automatically.

This decision supersedes the single-skill guidance in ADR 0001 and the explicit-request trigger in ADR 0004. It does not change their other decisions.

Ruling: Separate document structure, language, and plan workflow — each skill has one clear role, and users can install each skill by itself. Impact if wrong: agents may load overlapping guidance or omit STE review for non-plan documents.

Rejected alternatives:

1. Keep Diataxis and STE in one skill — this preserves the current overlap.
2. Put STE guidance in `writing-plans` — this limits the guidance to plans and changes a vendored upstream skill.
3. Update the Nix repository in this change — it is a separate repository with an independent manifest.

## Consequences

This repository has three complementary skills. Implementation plans use the Superpowers workflow and STE language guidance. Other technical documents can use STE without adopting the plan workflow.

Users who installed `ste-implementation-plans` must install `ste-technical-writing` to get the general STE guidance from this repository. The Nix repository continues to deploy its separate copy.
