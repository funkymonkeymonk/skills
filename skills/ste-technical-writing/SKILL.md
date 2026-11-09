---
name: ste-technical-writing
description: Use when creating, editing, or reviewing technical documentation, including ADRs, specifications, implementation plans, tutorials, how-to guides, and reference.
---

# STE Technical Writing

Use ASD-STE100 Issue 9 as a practical language guide for technical documentation. This skill governs language, not document structure or workflow. Use `diataxis-docs` to select structure for reader-facing documentation. Use `writing-plans` for implementation-plan structure and workflow. Use these skills together when they are available.

Apply STE to new technical content and to content that the user asks you to revise. Do not rewrite existing content only because it does not follow STE. Follow repository rules and preserve the purpose and scope of the requested change. If the user explicitly requests another style, use it for the prose. Do not impose STE word-choice or sentence-length rules on opted-out prose. Preserve technical accuracy, exact terms, and required document structure.

## Write in practical STE

- Use approved words with their approved meanings and parts of speech. Use established technical nouns and verbs when needed.
- Use the same term for the same component or concept throughout the document.
- Use active voice. In descriptive text, use passive voice only when the agent is unknown.
- In procedures, use the imperative. Give one instruction per sentence unless actions occur at the same time. State required conditions first.
- Keep procedural sentences to 20 words or fewer.
- Keep descriptive sentences to 25 words or fewer. Give each sentence and paragraph one topic. Keep paragraphs to six sentences or fewer.
- Use complete sentences. Do not use contractions or semicolons. Use vertical lists for complex content.
- Use American English spelling unless an official project rule requires another spelling.
- Preserve technical meaning, project terms, names, code, commands, quoted text, and interface labels. Do not replace a correct term to improve a lint score.
- Do not invent product behavior, requirements, options, or design rationale. Ask for missing facts or mark them as unknown.

These practices reflect ASD-STE100 Issue 9. They are guidance for technical prose, not a claim of full standard conformance.

## Check the prose

When `ste` is available, check authored Markdown with:

```bash
ste lint --mode=flavored --format=agent --no-config path/to/file.md
```

For an unsaved draft, pipe its text to `ste lint --mode=flavored --format=agent --no-config` without a file path. With no paths, `ste` reads standard input. The `--no-config` option prevents a target repository's score threshold from turning this advisory review into a pass/fail gate.

Review every finding. Fix a finding only when the change preserves meaning and improves clarity. Flavored mode does not check words against the STE dictionary. Treat lint results as advisory. Do not claim formal STE certification.

If the user requests a strict dictionary check, use `ste dict build --pdf <local-issue-9-pdf>` only when a local Issue 9 PDF is available. Keep the index in the user's cache. Do not add the PDF or generated index to the repository. Review dictionary findings in context because STE permits technical nouns and verbs that are not in its dictionary.

If `ste` is unavailable, review the prose manually and state that the linter did not run. Do not install tools during writing.
