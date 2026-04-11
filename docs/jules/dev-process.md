# Decoupling Operational Workflows from System Development

## Problem: Context Dilution & Token Bloat

During the development of the wiki's extension for novel-author workflows, it became clear that the agent instruction files (`CLAUDE.md` and `GEMINI.md`) serve two fundamentally conflicting purposes:

1. **The Operational Persona (The Writer/Researcher):** An agent acting as the wiki's operator only needs to know how to ingest files, query the graph, draft chapters, and manage reader state.
2. **The Developer Persona (The System Builder):** An agent acting as the wiki's maintainer needs to know the schema specs, the `docs/` architecture, the phase roadmaps in `todo/`, and the meta-maintenance rules.

Currently, these two roles are compressed into single, monolithic instruction files (`CLAUDE.md`, `GEMINI.md`). When a user asks the agent to "ingest this source file", the agent is burdened with parsing instructions about the Phase 5 Writing Pipeline, Dramatica integration, and rules for marking `todo` checklists.

**This causes three major problems:**
1. **Token Inefficiency:** We are wasting the context window on irrelevant system architecture when the agent just needs to perform a simple operational task.
2. **Instruction Confusion:** The agent might hallucinate development workflows while trying to execute operational workflows (or vice versa).
3. **Scaling Bottleneck:** As the system grows, the single `.md` file becomes unwieldy, violating the core principle of progressive disclosure.

## Proposed Solution: The Two-Agent Model

We must separate the instructions into two explicit personas: **WikiOps** and **SysDev**.

### 1. WikiOps (Operational Context)

**Purpose:** Daily usage of the wiki (ingesting, writing, querying).
**Context Load:** Minimal. Fast.
**Structure:**
- Keep `CLAUDE.md` and `GEMINI.md` extremely lean.
- They should *only* define the operational slash commands (`/wiki-ingest`, `/wiki-chapter`, etc.) and the basic directory layout (`raw/`, `processed/`, `wiki/`).
- They should rely heavily on the Discovery Hooks (`wiki/meta/discovery-protocol.md`) to pull in only the necessary pages at runtime.
- **Remove all references to the `todo/` directory and development roadmaps.**

### 2. SysDev (Development Context)

**Purpose:** Extending the wiki architecture, implementing new phases, modifying schemas.
**Context Load:** Deep, structural.
**Structure:**
- Create a dedicated trigger or persona initialization, e.g., `/sysdev` or *"Activate Developer Mode"*.
- When activated, the agent reads a new root file: `DEVELOPER.md`.
- `DEVELOPER.md` contains the rules for modifying the system: reading the `todo/` roadmaps, understanding the `docs/` schemas, and following the session start protocols.

## Implementation Steps (Future Work)

1. **Refactor CLAUDE.md / GEMINI.md:** Strip out the "Development Roadmap" section and the "Session Start Protocol". Keep only the "Slash Commands", "Directory Layout", and "Ingest/Query/Lint/Graph" basic operations.
2. **Create DEVELOPER.md:** Move the stripped-out development instructions here.
3. **Establish Context Boundaries:** Explicitly instruct the agent in `CLAUDE.md` that if the user asks to modify the system structure (e.g., "add a new page type", "implement Phase 4"), it must *first* read `DEVELOPER.md` to load the development context.

## Benefits

- **Massive Token Savings:** The vast majority of daily interactions (WikiOps) will run with a fraction of the context overhead.
- **Improved Accuracy:** The agent will focus solely on the immediate operational task, guided by the specific `SKILL.md` for that workflow, without being distracted by system architecture rules.
- **Cleaner Progressive Disclosure:** The system achieves true progressive disclosure at the persona level, not just the file level.
