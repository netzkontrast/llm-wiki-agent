# Split System Development from Operational Workflows

## The Problem
Currently, the main entry files (`CLAUDE.md` and `GEMINI.md`) serve a dual purpose. They hold:
1. **Operational Workflows:** Directives on how an agent should use the wiki (ingesting, querying, writing chapters, reading constraints).
2. **System Development:** Instructions on how the *developer* agent should build the repository (phases, todo tasks, hygiene rules).

This mixed context balloons the core system prompt, causing context dilution. During an active writing session (e.g., generating manuscript prose), the agent does not need to know about "Phase 6 Token-efficient ingest" or the rules for updating `todo/README.md`.

## Proposed Solution
Separate these concerns into two distinct modes or entry points.

### 1. The Operational Agent (Author/Editor)
*   **Entry Point:** `CLAUDE.md` / `GEMINI.md`
*   **Scope:** Contains only the rules for writing, reading the schema, running `tools/ingest.py` or `/wiki-chapter`, progressive disclosure principles, and the contradiction hierarchy.
*   **Benefits:** Faster response times, less token consumption, and zero hallucination of "development tasks" when it should be focusing on narrative generation.

### 2. The Systems Architect (Developer)
*   **Entry Point:** A new file, e.g., `CLAUDE_DEV.md` or a specific section within the `docs/jules/` directory that is invoked manually.
*   **Scope:** Contains the `todo/` tracker, Phase status, meta-maintenance rules, and architectural design decisions.
*   **Benefits:** Can be activated only when expanding the repository's toolset or schema, preventing contamination of story logic with python scripting tasks.

## Implementation Path
- Refactor `CLAUDE.md` to strictly outline the 15 page types, 4 layers, and 13 slash commands.
- Move the "Development Roadmap (todo/)" and "Universal Rules" sections into a dedicated developer file.
- Implement an explicit "switch" where an agent is told "You are in Dev Mode" vs "You are in Writing Mode".
