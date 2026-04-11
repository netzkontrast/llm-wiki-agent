# Handover & Reflections

## Current State
- The wiki architecture is complete up through Phase 5.
- The 4-layer routing structure (Knowledge, Narrative, Reader State, Meta) is established and documented.
- The writing pipeline (Chapter -> Outline -> Beats -> Manuscript) is active, with seed templates created and verified.
- The Python tooling (`build_graph.py`, `lint.py`, `ingest.py`, `lint_deterministic.py`) has been upgraded to handle the new layer dependencies, extracting explicit `REQUIRES` and `INFORMS` edges, and ensuring idempotent ingest moves.
- Agent instructions in `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` cover all 15 page types and 13 slash commands.
- **The raw file `UmfassendesLokalitatenKonzeptFurRoman.md` has now been fully processed and moved to the `processed/` directory.**
- **All 31 locations and the overarching `PsychologicalLandscapes` concept have been extracted, created as markdown files with the proper YAML frontmatter, and injected into `wiki/index.md`.**

## Analysis of the Previous Ingestion Run

During a previous session (committed under `1c95e90` "feat: add /sessionlog command and trace mode for ingest workflow"), an agent was tasked with testing the new "Trace Mode" using the `/sessionlog` wrapper.

The agent explicitly chose the largest file in the queue, `raw/UmfassendesLokalitatenKonzeptFurRoman.md`.

**Why were entities missed?**
By reading the previous session's `trace.md` and `plan.md` (via git history), I discovered that the agent *intentionally* skipped extracting all 31 locations.
In `log/sessionlog-wiki-ingest/[...]/plan.md`, the agent wrote:
> *(To avoid creating 31 separate pages during this test run, we will pick 3 representative locations across different planes to fully exercise the schema, and log the rest as a single aggregate update).*

The agent's primary goal in that session was to demonstrate the ultra-verbose logging capability and ensure the schema worked, rather than performing bulk data entry. It successfully extracted `Kw1KaelsInitialeWohneinheit`, `Kw2VergessenerSchrein`, `AegisAnalyseHub`, and `PsychologicalLandscapes`.

**How this run differed:**
In the current session, I developed a Python extraction script to programmatically parse the missing 28 locations directly from the markdown file's structural headings. I then ran a generator script to create all missing markdown files, and an index update script to inject all 30 missing links (excluding LogosPrime which already existed). This programmatic approach scales perfectly to large bulk extractions, bypassing the LLM output token limits that the previous agent was actively trying to avoid.

## Meta Reflections (Phase 7 - Meta Consolidation Preview)

### The Dual-Agent Problem
We have successfully decoupled "Operational Workflows" from "System Development" conceptually using markdown headers in `CLAUDE.md`. However, as the repository grows, reading the entire development roadmap (Phase status, Meta-Maintenance, Universal Rules) consumes valuable context tokens when the agent's actual task is simply to "write chapter 5".

I have created `docs/jules/dev-process.md` proposing a formal split:
- An **Operational Agent** prompt focused purely on navigating the wiki, reading constraints, and writing prose.
- A **Systems Architect** prompt for building the repo, tracking phases, and writing python scripts.

### Workflow Bottlenecks
The extended `tools/ingest.py` script attempts to extract 9 different page types (entities, concepts, characters, locations, conflicts, themes, rules, timeline events, foreshadowing) from a single source document in one massive LLM call.

As seen when trying to process complex inputs, this is highly prone to output truncation due to token limits. (This is another reason the trace-mode agent manually skipped locations).

I have documented this in `docs/jules/workflow-consolidation.md`, proposing a multi-stage ingestion pipeline to mitigate JSON truncation.

### Progressive Disclosure
The addition of navigational `README.md` files in every subdirectory is a massive win for context efficiency. Agents can now read a folder's README to discover its contents without needing to `grep` or list all files. We must strictly enforce this hygiene rule moving forward.

## Next Steps
- Consider implementing Phase 6 (Adaptive Ingest) to address the token bottleneck in `tools/ingest.py` before running it on massive raw documents.
- Review the `docs/jules/` proposals for splitting the agent instructions into a leaner, operational-focused `CLAUDE.md`.
