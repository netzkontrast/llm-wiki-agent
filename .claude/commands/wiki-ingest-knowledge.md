---
name: wiki-ingest-knowledge
description: knowledge layer ingest
---

Writes: `knowledge/sources/`, `knowledge/entities/`, `knowledge/concepts/`, `knowledge/rules/`, `knowledge/timeline/`, `knowledge/syntheses/`
Context: qmd `-c knowledge` only; ceiling 10 pages
Model target: Haiku (factual extraction, structured schema, predictable)
Used by Gemini Jules for autonomous batch ingest
Merge rule: always update `sources:` field; append new facts only
