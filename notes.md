# Reflections on the Ingestion Process and Workflow Improvements

The initial task involved establishing a clear ingestion workflow by moving the queue of raw files to a dedicated `to-Ingest.md` file, updating the agent instructions, and then manually ingesting the first few files. We later added a crucial constraint to ensure all generated wiki output is in English, while keeping the original slugs for traceability.

Based on this experience, here are several reflections and actionable improvements to enhance the ingestion process:

## 1. Manual vs. Automated Ingestion
**Observation:**
Currently, the ingestion workflow is being executed manually step-by-step by the LLM agent: reading the raw file, synthesizing the summary, creating individual concept and entity pages, and then meticulously updating `overview.md`, `index.md`, and `log.md`. This is prone to human/agent error, such as forgetting to update an internal wikilink, or creating duplicate concepts (e.g., `[[OriginEgo]]` vs `[[Ursprungs-Ich]]`).

**Improvement:**
The repository contains a `tools/ingest.py` script designed to automate this entire process via the Anthropic API.
*   **Recommendation:** Instead of having the agent manually execute the 9-step ingestion workflow for each file, the agent should primarily rely on executing `python tools/ingest.py <path-to-raw-file>`. This script programmatically guarantees that the index, overview, log, and respective concept/entity files are updated consistently in one atomic action.

## 2. Queue Management (`to-Ingest.md`)
**Observation:**
The queue is currently a static markdown file where lines are manually deleted after processing. When multiple files are ingested sequentially, deleting lines using `sed` or manually rewriting the file can become tedious and error-prone.

**Improvement:**
*   **Recommendation:** We could build a small wrapper script (e.g., `process_queue.sh` or `tools/batch_ingest.py`) that reads the top line of `to-Ingest.md`, passes it to `tools/ingest.py`, and then automatically pops that line from the file. This would allow for seamless batch processing (e.g., "Ingest the next 5 files") without the agent needing to manually track and modify the text file at every step.

## 3. Language Constraints & State Drift
**Observation:**
The introduction of the "English-Only" rule mid-way through ingestion highlighted how easily state drift can occur. When we translated existing German concepts (like `KohärenzProtokoll` to `CoherenceProtocol`), several internal wikilinks in already-processed source pages broke because they were hardcoded to the German names.

**Improvement:**
*   **Strict Prompting:** The `tools/ingest.py` and `tools/query.py` scripts have been updated to heavily emphasize the language constraint.
*   **Recommendation (Linting):** The `tools/lint.py` (or `/wiki-lint` workflow) should be run frequently, ideally as a pre-commit hook or after every batch of ingestions. The linting tool is specifically designed to catch broken links, orphans, and stale summaries. Running this proactively would immediately flag if a concept was translated inconsistently (e.g., linking to `[[CoherenceProtocol]]` but creating `[[TheCoherenceProtocol.md]]`).

## 4. Context Window & Overview Synthesis
**Observation:**
As more files are ingested, `wiki/overview.md` is continually rewritten to synthesize the entire repository. Currently, the LLM reads the *entire* raw source document and the *entire* current overview to rewrite it.

**Improvement:**
*   **Recommendation:** As the wiki grows, injecting all recent sources and the full overview into the context window will become expensive and eventually hit token limits. The overview update process should eventually be decoupled from the individual file ingestion, perhaps becoming a nightly/weekly cron job (e.g., a dedicated `tools/synthesize.py`) that reads only the *summaries* of the source files rather than the raw text to generate the high-level synthesis.

## Summary of Action Plan for Next Sessions
1.  **Shift to Tooling:** Prioritize using `python tools/ingest.py <file>` for future ingestions rather than manual agent drafting.
2.  **Automate Queue:** Consider writing a simple bash loop to process `to-Ingest.md` automatically.
3.  **Lint Regularly:** Run `/wiki-lint` or `python tools/lint.py` after every session to catch broken translated links or contradictions early.
