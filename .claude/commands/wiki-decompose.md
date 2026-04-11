---
name: wiki-decompose
description: per-file planning skill
---

Trigger: "/wiki-decompose raw/foo.md" or before any interactive ingest session
The agent must read the FULL contents of the source file itself using its natural language understanding. Do not use external scripts or regex to decompose.

Use the following clustering rules to identify entities accurately:
- **Locations/Items**: Any distinct place, area, setting, artifact, or object mentioned in the text.
- **Characters/Entities**: Any named person, alter, persona (e.g., Limina, Echo, Index, Nox), AI system, or organization.
- **Concepts**: Any thematic concept, world-structural system, rule, or category described in the text.

You MUST extract a FULL and EXHAUSTIVE inventory. It is strictly forbidden to cap the entity list (e.g., no "top 5" or "representative sample"). All entity counts must be honored during ingest.

Generate the approved plan and save it to `log/{branch}/{session}/plan.md` in the following structure:
1. A clear, bulleted inventory of all extracted entities, grouped by type (e.g., `### Locations`, `### Characters`, `### Concepts`). Each bullet should specify the target page (e.g., `- [Entity Name] -> wiki/narrative/locations/[Entity Name].md`). The entities should not contain markdown styling like bold (`**`).
2. Layers touched (knowledge, narrative, reader_state).
3. Known vs. new entities and qmd search commands to run.
4. A `## Summary` block with counts for each category and a TOTAL entities count.

If the plan contains > 10 TOTAL entities, add a BATCH MODE flag to the plan file.
SPARK-influenced: asks "what in this file's framing could be wrong or misleading?"
Output: a validated per-file ingest plan, ready for `/wiki-ingest` execution.
