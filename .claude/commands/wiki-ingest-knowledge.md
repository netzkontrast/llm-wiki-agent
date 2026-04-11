---
name: wiki-ingest-knowledge
description: knowledge layer ingest
---

## EXHAUSTIVE EXTRACTION
Extract EVERY entity (persons, systems, organizations), concept, rule. No entity may be deferred.
Create entity pages in `knowledge/entities/` for ALL named persons, AI systems, organizations, or world-structural systems encountered — not just prominent ones.

Writes: `knowledge/sources/`, `knowledge/entities/`, `knowledge/concepts/`, `knowledge/rules/`, `knowledge/timeline/`, `knowledge/syntheses/`
Context: qmd `-c knowledge` only; ceiling 10 pages
Model target: Haiku (factual extraction, structured schema, predictable)
Used by Gemini Jules for autonomous batch ingest
Merge rule: always update `sources:` field; append new facts only
