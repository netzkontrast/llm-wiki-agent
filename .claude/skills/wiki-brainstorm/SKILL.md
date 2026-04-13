---
name: wiki-brainstorm
description: Executes the wiki-brainstorm capability. Use when triggered. Use when the user requests wiki-brainstorm or related tasks.
---

# wiki-brainstorm

# /wiki-brainstorm

**Triggers:** "brainstorm about X", "explore idea X", "what if X", "research X for the novel", "how could X work"

Use this workflow for exploratory generation, synthesis of ideas, and what-if scenario planning without immediately modifying canonical knowledge.

## Reference
See `docs/agent-workflows.md` for detailed specifications.

## Workflow Execution

1.  **Temporal Filter:** None (brainstorming is atemporal).
2.  **Context Loading:**
    *   Read `wiki/overview.md` for global context.
    *   Load concept/theme pages matching the brainstorming topic.
    *   Load source pages relevant to the topic.
    *   Load entity pages if the topic involves real-world references.
    *   Apply a context ceiling of 15 pages.
3.  **Output Generation:**
    *   Provide a synthesis of relevant wiki knowledge applied to the brainstorming question.
    *   Optionally propose new concept, theme, or synthesis pages if the ideas are mature.
    *   Prompt the user to confirm if the output should be saved as a synthesis page (`wiki/syntheses/"[slug]".md`).
4.  **Validation:**
    *   Check proposed ideas against existing rule pages for potential contradictions.
    *   Cross-reference with existing concept pages to avoid duplication.
    *   Flag any ideas that would require modifying fundamental world rules.


## Gotchas
- When performing semantic synthesis, ensure you do not drop critical nuance or factual quotes from the L0 node.
- If data contradicts between the current L0 node and an existing L2 concept page, NEVER overwrite the L2 page silently. Always use `[!contradiction]` blocks.
- Ensure any file created strictly conforms to its respective page type layout in `docs/wiki-schema.md`.
