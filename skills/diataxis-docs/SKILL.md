---
name: diataxis-docs
description: Use when creating, editing, reviewing, or organizing technical documentation, specifications, ADRs, plans, tutorials, how-to guides, reference, or explanations.
---

# Diataxis Documentation

Use this skill for documentation work from any workflow or skill. Follow the repository's `AGENTS.md` and existing conventions for file locations. Keep the active workflow intact.

Use STE unless the user explicitly requests another style. Apply this rule to specifications, ADRs, plans, and all other documentation. When you read existing documents, use them as source material. Do not rewrite them only because they are not in STE.

## Choose a Diataxis form

Classify each document by the reader's need:

- **Tutorial:** Guide a learner through a practical experience. The reader learns by doing.
- **How-to guide:** Help a capable user complete a real task. Give direct, adaptable steps.
- **Reference:** State accurate, complete, neutral facts. Match the product structure.
- **Explanation:** Give context, concepts, and rationale. Explain why or how ideas relate.

Give each document one primary purpose. A document can include brief context when it helps the primary purpose. If a request combines distinct needs, identify them. Ask before a major restructure when the user requests one document. Otherwise, separate the content and add useful cross-references.

Do not turn reference facts into instructions. Do not put detailed rationale in tutorials or how-to guides. Do not use explanations as reference lists. Keep examples accurate and relevant to the document's purpose.

## Write in STE

Use ASD-STE100 Issue 9 as the default language standard. Follow these rules:

- Use approved words with their approved meanings and parts of speech. Use established technical nouns and verbs when needed.
- Use the same term for the same concept. Follow the project's approved terminology.
- Use active voice. In descriptive text, use passive voice only when the agent is unknown.
- In procedures, write instructions in the imperative. Use one instruction per sentence unless actions occur at the same time. Put required conditions first.
- Keep procedural sentences to 20 words or fewer.
- In descriptive text, keep each sentence to 25 words or fewer. Give each sentence and paragraph one topic. Keep paragraphs to six sentences or fewer.
- Use complete sentences. Do not use contractions or semicolons. Use vertical lists for complex content.
- Use American English spelling unless an official project rule requires another spelling.

Preserve technical meaning and exact project terms, names, code, commands, quoted text, and interface labels. Do not replace a correct term to improve a lint score. Do not invent product behavior, requirements, options, or design rationale. If the source lacks a required fact, ask for it or mark it as unknown.

## Check the prose

When `ste` is available, check authored Markdown with:

```bash
ste lint --mode=flavored --format=agent --no-config path/to/file.md
```

Review each finding. Fix it only when the change keeps the intended meaning. Flavored lint does not check words against the approved dictionary. Use dictionary checks only when a local Issue 9 index is available. Treat all lint results as advisory. Do not claim formal STE certification.

Do not include the ASD-STE100 PDF or a generated dictionary index in a skill package.
