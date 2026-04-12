# Tools

Standalone deterministic Python scripts for maintaining the wiki. These tools do not make external API calls.

## Scripts
- `chunk.py <source-file>` — Semantically chunks raw source files for the ingest chunk loop.
- `compile_context.py --task <task>` — Compiles structured markdown contexts for agent LLM invocations.
- `validate.py` — Wraps `lint_deterministic.py` to add schema validation logic.
- `index_manager.py <command>` — Machine-readable CLI for manipulating `wiki/index.md`.
- `build_graph.py` — Builds the knowledge graph. Run with `--open` to open in browser. Use `--infer` to activate agent semantic edge inference.
- `lint_deterministic.py` — Enforces structural and schema rules offline.
- `check_staleness.py` — Utility script.
- `install-qmd.sh` — Installs qmd and sets up the wiki collections and contexts.
- `session_init.py` — Initializes a logging session folder for adaptive ingest.
