# Phase 7: Meta Consolidation & Workflow Efficiency

**Status:** `active`
**Prerequisites:** Phase 5 complete
**Spec references:** `docs/jules/dev-process.md`, `docs/jules/workflow-consolidation.md`

## Purpose

The repository has grown significantly in complexity. The primary goal of Phase 7 is to address token bloat and workflow navigation friction discovered during the implementation of the novel-writing pipeline. We need to structurally separate the instructions for an "Operational Agent" (authoring chapters, reading the wiki) from the "Systems Architect" (tracking phases, updating python scripts, managing hygiene). Additionally, we need to address the risk of JSON truncation during massive raw document ingestion.

---

## Tasks

### Agent Instruction Decoupling

- [ ] 1. Create `CLAUDE_DEV.md` (or similar file) to house the "System Development" and "Development Roadmap (todo/)" sections currently bloating `CLAUDE.md`.
- [ ] 2. Strip `CLAUDE.md` down to only operational workflows (ingest, query, lint, graph, novel-writing slash commands).
- [ ] 3. Update the `Session Start Protocol` to require checking `CLAUDE_DEV.md` only when specifically asked to perform a developer task or advance a phase.
- [ ] 4. Apply the same decoupling logic to `GEMINI.md` and `AGENTS.md`.

### Ingest Workflow Refactoring

- [ ] 5. Refactor `tools/ingest.py` to use a multi-stage LLM processing pipeline to prevent JSON truncation on large inputs.
- [ ] 6. Pass 1: Summarize and extract standard Knowledge Layer elements (Concepts, Entities, Sources).
- [ ] 7. Pass 2: Extract Narrative Layer elements (Characters, Locations, Conflicts, Themes).
- [ ] 8. Pass 3: Extract Structural elements (Rules, Timeline, Foreshadowing).
- [ ] 9. Update the Ingest Workflow documentation to reflect the new multi-stage pipeline logic.

### Progressive Disclosure Enforcement

- [ ] 10. Implement a deterministic lint check in `tools/lint_deterministic.py` that verifies every directory under `wiki/` contains a valid `README.md` file.
- [ ] 11. Ensure that any newly created pages or directories automatically generate or update their respective `README.md`.

### Context Budgeting

- [ ] 12. Create `tools/estimate_context.py` to calculate the approximate token weight of a given page and its depth-1 dependencies.
- [ ] 13. Update slash commands to dynamically use `estimate_context.py` to adhere strictly to Context Ceilings rather than arbitrary page counts.

---

## Completion Criteria

- `CLAUDE.md` is strictly an operational manual.
- Developer instructions and Phase tracking live in a dedicated dev-focused entry point.
- `tools/ingest.py` handles massive files robustly via multi-stage extraction.
- A directory README lint check exists.
- The `todo/README.md` phase table is updated with Phase 7 complete.
