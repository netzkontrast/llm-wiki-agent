# Tools

Optional standalone Python scripts for maintaining the wiki. These tools require `ANTHROPIC_API_KEY` for full functionality (semantic steps), but deterministic steps run locally.

## Scripts
- `build_graph.py` — Builds the knowledge graph. Run with `--open` to open in browser. Run with `--no-infer` to skip semantic edge inference.
- `lint.py` — Runs a health check on the wiki. Calls `lint_deterministic.py` first, then performs semantic contradiction checks via Claude API.
- `lint_deterministic.py` — Enforces structural and schema rules offline.
- `ingest.py <path>` — Ingests a raw file into the wiki using the LLM. (Requires qmd to be installed)
- `check_staleness.py` — Utility script.
- `query.py` — Legacy query script.
- `install-qmd.sh` — Installs qmd and sets up the wiki collections and contexts.
- `decompose.py` — Evaluates a raw file and generates an ingest plan.
- `session_init.py` — Initializes a logging session folder for adaptive ingest.
