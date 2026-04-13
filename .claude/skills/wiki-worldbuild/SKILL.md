---
name: wiki-worldbuild
description: Executes the wiki-worldbuild capability. Use when triggered. Use when the user requests wiki-worldbuild or related tasks.
---

# wiki-worldbuild

# /wiki-worldbuild

**Triggers:** "build world element X", "develop location X", "define rule X", "world-building for X", "how does X work in this world"

Use this workflow to develop locations and rules that define the mechanics and setting of the novel.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** If a chapter context is provided, apply the temporal filter. Otherwise, no temporal filtering.
2.  **Context Loading:**
    *   Read the target location or rule page.
    *   Load connected characters (from location's `Connected Characters` or rule's `chapter_relevance`).
    *   Load timeline events providing historical context.
    *   Load other rule pages in the same `domain` for consistency.
    *   Load other locations in the same `world` for coherence.
    *   Apply a context ceiling of 10 pages.
3.  **Output Generation:**
    *   Update or create the target location or rule page.
    *   Flag any inconsistencies with existing world rules.
    *   Update `informs:` targets if the changes affect chapters.
4.  **Validation:**
    *   Ensure new rules do not contradict existing rules in the same domain.
    *   Ensure locations are internally consistent with their `world` grouping.
    *   Log any changes that affect existing chapter content.
