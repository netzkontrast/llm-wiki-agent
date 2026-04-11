---
name: wiki-ingest
description: Orchestrates ingest sub-skills.
---

This skill is an orchestrator. It does NOT write pages directly.
Token budget note: orchestrator context ceiling 5 pages.

Steps:
1. Run `/wiki-decompose` to determine layers touched.
2. Determine layers touched from the plan.
3. Call sub-skills (`/wiki-ingest-knowledge`, `/wiki-ingest-narrative`, etc) in order.
4. Update `wiki/index.md` (all sections).
5. Append `wiki/log.md`.
6. Move file from `raw/` to `processed/`.
