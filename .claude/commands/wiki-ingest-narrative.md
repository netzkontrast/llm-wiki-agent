---
name: wiki-ingest-narrative
description: narrative layer ingest
---

## EXHAUSTIVE EXTRACTION
Extract EVERY named location, character, alter, persona. Never create a 'representative' subset.

## BATCH GUIDANCE
If the plan lists N > 6 entities of the same type, process them 6 at a time. Run this skill repeatedly, advancing through the list, until the plan inventory is exhausted.

## ALTER/PERSONA DETECTION
Named alters in DID character descriptions (e.g., Limina, Echo, Index, Nox) are characters and require their own character pages.

## COMPLETION CHECK
Before finishing, read the plan's entity count for locations and characters and verify the number of files written matches.

Writes: `narrative/characters/`, `narrative/locations/`, `narrative/conflicts/`, `narrative/themes/`, `narrative/arcs/`, `narrative/dramatica/`, `narrative/timeline/`
Context: qmd `-c narrative` + any known entity pages from decompose plan; ceiling 15 pages
Model target: Sonnet (relationship complexity, merge logic)
Interactive preferred; autonomous only for well-structured sources
Merge rule: merge character profiles; never overwrite established traits without contradiction log entry
