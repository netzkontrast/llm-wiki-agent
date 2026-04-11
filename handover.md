# Handover & Reflections

## Current State
- The wiki architecture is complete up through Phase 5.
- The 4-layer routing structure (Knowledge, Narrative, Reader State, Meta) is established and documented.
- The writing pipeline (Chapter -> Outline -> Beats -> Manuscript) is active, with seed templates created and verified.
- The Python tooling (`build_graph.py`, `lint.py`, `ingest.py`, `lint_deterministic.py`) has been upgraded to handle the new layer dependencies, extracting explicit `REQUIRES` and `INFORMS` edges, and ensuring idempotent ingest moves.
- Agent instructions in `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` cover all 15 page types and 13 slash commands.

## Meta Reflections (Phase 7 - Meta Consolidation Preview)

### The Dual-Agent Problem
We have successfully decoupled "Operational Workflows" from "System Development" conceptually using markdown headers in `CLAUDE.md`. However, as the repository grows, reading the entire development roadmap (Phase status, Meta-Maintenance, Universal Rules) consumes valuable context tokens when the agent's actual task is simply to "write chapter 5".

I have created `docs/jules/dev-process.md` proposing a formal split:
- An **Operational Agent** prompt focused purely on navigating the wiki, reading constraints, and writing prose.
- A **Systems Architect** prompt for building the repo, tracking phases, and writing python scripts.

### Workflow Bottlenecks
The extended `tools/ingest.py` script attempts to extract 9 different page types (entities, concepts, characters, locations, conflicts, themes, rules, timeline events, foreshadowing) from a single source document in one massive LLM call.

As seen when trying to process complex inputs, this is highly prone to output truncation due to token limits.

I have documented this in `docs/jules/workflow-consolidation.md`, proposing a multi-stage ingestion pipeline to mitigate JSON truncation.

### Progressive Disclosure
The addition of navigational `README.md` files in every subdirectory is a massive win for context efficiency. Agents can now read a folder's README to discover its contents without needing to `grep` or list all files. We must strictly enforce this hygiene rule moving forward.

## Next Steps
- Consider implementing Phase 6 (Adaptive Ingest) to address the token bottleneck in `tools/ingest.py` before running it on massive raw documents.
- Review the `docs/jules/` proposals for splitting the agent instructions into a leaner, operational-focused `CLAUDE.md`.
