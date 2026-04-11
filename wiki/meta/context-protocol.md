# Context Ceiling Protocol

This document outlines the hard page-count ceiling protocol. Agents must follow this protocol to enforce page limits per workflow.

## Drop Protocol

1. Count the number of pages loaded into context **after** applying the temporal filtering.
2. Check the workflow's specific page ceiling against this count.
3. If the count exceeds the ceiling, start dropping pages according to the priority-drop order defined for the workflow (from first to last category).
4. Within a category, drop the page with the **fewest connections** to the target page first.
5. Continue dropping pages until the count is less than or equal to the ceiling.
6. Log any dropped pages in the agent's working notes so they can be retrieved if requested by the user.

## Workflow Ceilings and Priority Drop Order

| Workflow | Ceiling | Priority Drop (shed first → last) |
|----------|---------|-----------------------------------|
| chapter-writing | 20 | themes → older conflicts → locations not in current scene |
| character-dev | 10 | chapter summaries → distant arc stages |
| revision | 30 | themes → dramatica → distant timeline events |
| lectoring | 15 | arcs → dramatica → non-POV characters |
| world-building | 10 | timeline events → arcs → distant locations |
| conflict-resolution | 15 | dramatica → distant timeline events |
| reader-model | 10 | reinforced foreshadowing → distant reader-states |
| brainstorming | 15 | oldest sources → distant entities |
