---
name: wiki-decompose
description: Executes the following: per-file planning skill. Use when the user requests wiki-decompose or related tasks.
---

# wiki-decompose

Trigger: "/wiki-decompose chunks/foo/0001_chunk.md" or before any interactive ingest session

1. Run `python3 tools/compile_context.py --task plan --chunk "[path-to-chunk]"`
2. Read the compiled context. You receive a pre-compiled context. Do NOT read wiki/index.md yourself.
3. Use the following clustering rules to identify entities accurately:
   - **Locations/Items**: Any distinct place, area, setting, artifact, or object mentioned in the text.
   - **Characters/Entities**: Any named person, alter, persona (e.g., Limina, Echo, Index, Nox), AI system, or organization.
   - **Concepts**: Any thematic concept, world-structural system, rule, or category described in the text.
   - **Relationships**: Identify direct relationships, connections, or interactions between any of the extracted entities.
   - **Contradictions**: Identify any statements that contradict established lore or represent internal conflicts within the chunk.

You MUST extract a FULL and EXHAUSTIVE inventory. It is strictly forbidden to cap the entity list (e.g., no "top 5" or "representative sample"). All entity counts must be honored during ingest.

Generate the approved plan and save it to `wiki/meta/ingest/"[slug]"-plan.md` in the following structure:
1. A clear, bulleted inventory of all extracted entities, grouped by type (e.g., `### Locations`, `### Characters`, `### Concepts`). Each bullet should specify the target page (e.g., `- [Entity Name] -> wiki/narrative/locations/[Entity Name].md`). The entities should not contain markdown styling like bold (`**`).
2. A `### Relationships` block detailing connections to map in frontmatter (e.g., `- [Kael] -> related_entities: ["Juna", "Lex"]`).
3. A `### Contradictions` block if any are found, to be logged in the meta registers.
4. Layers touched (knowledge, narrative, reader_state).
5. A `## Summary` block with counts for each category and a TOTAL entities count.

If `compile_context.py` injected a Batch Processing Instruction, honor it.
SPARK-influenced: asks "what in this file's framing could be wrong or misleading?"
Output: a validated per-chunk ingest plan, ready for `/wiki-ingest` execution.
