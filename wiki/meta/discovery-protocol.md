# Discovery Protocol (Hooks)

This document describes the Discovery Hook mechanism used in the novel-writing agent workflows, specifically the `chapter-writing` workflow.

## Purpose

To manage the context window effectively and prevent irrelevant information from diluting the agent's focus, the Discovery Hook limits context loading to *only* what is explicitly referenced in the target chapter's frontmatter.

## Mechanism

Before executing the core logic of the `chapter-writing` workflow, the agent must perform the following discovery steps:

1.  **Read Target Frontmatter:** Parse the YAML frontmatter of the target chapter page (`wiki/chapters/chapter-NN.md`).
2.  **Extract References:** Extract the lists of referenced entities from the following fields:
    *   `characters:`
    *   `locations:`
    *   `conflicts:`
    *   `constraint_refs:`
3.  **Targeted Context Load:** Load *only* the pages corresponding to the extracted references from `wiki/knowledge/`.
    *   Do *not* load the entire `wiki/knowledge/` directory.
    *   Do *not* load pages related to the chapter indirectly unless specifically required by another step in the workflow (e.g., following a `requires:` link to depth 2, subject to the context ceiling).
4.  **Proceed with Workflow:** Continue with the remaining context loading steps (e.g., temporal filtering, reader-state loading) as defined in the workflow specification.
