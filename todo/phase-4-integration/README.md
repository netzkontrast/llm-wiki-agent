# Phase 4: CLAUDE.md Integration & Migration

**Status:** `complete`
**Prerequisites:** Phase 3 complete
**Spec references:** `docs/wiki-schema.md`, `docs/agent-workflows.md`, `docs/navigation-system.md`

## Purpose

Integrate all novel-specific extensions into the main CLAUDE.md instruction file. Update the page format, directory layout, ingest workflow, lint workflow, graph workflow, index format, and naming conventions. Update AGENTS.md and GEMINI.md for cross-agent consistency. Migrate any existing wiki content to the new schema.

---

## Tasks

### CLAUDE.md Updates

- [x] 1. Update the **Directory Layout** section in CLAUDE.md to include all 13 new directories (characters, chapters, locations, conflicts, themes, timeline, rules, arcs, dramatica, reader-model, foreshadowing, archive, meta)
- [x] 2. Update the **Page Format** section to show the full standard fields: `requires`, `informs`, `valid_from`, `valid_until`, `traits` — alongside the existing `title`, `type`, `tags`, `sources`, `last_updated`
- [x] 3. Update the **type** enum to include all 15 types: `source | entity | concept | synthesis | character | chapter | location | conflict | theme | timeline-event | rule | arc | dramatica | reader-state | foreshadowing`
- [x] 4. Update the **Ingest Workflow** to include extended steps 10-17 (create novel-specific pages during ingestion)
- [x] 5. Update the **Lint Workflow** to include novel-specific checks: orphan characters, timeline gaps, foreshadowing with no resolution, constraint_refs to non-existent rules, terminology_permitted ratchet violations
- [x] 6. Update the **Graph Workflow** to extract `requires:/informs:` edges alongside `[[wikilinks]]`
- [x] 7. Update the **Index Format** to show all 15 sections
- [x] 8. Update the **Naming Conventions** to cover all new page types
- [x] 9. Add the **Slash Commands** table entries for the 9 new commands (wiki-chapter, wiki-character, wiki-worldbuild, wiki-timeline, wiki-conflict, wiki-reader-model, wiki-revise, wiki-lector, wiki-brainstorm)

### Cross-Agent Schemas

- [x] 10. Update `AGENTS.md` with the essential novel-specific extensions (simplified, as per existing pattern — AGENTS.md is ~60% of CLAUDE.md complexity)
- [x] 11. Update `GEMINI.md` with minimal novel-specific extensions (as per existing pattern — GEMINI.md is ~45% of CLAUDE.md complexity)

### Migration

- [x] 12. If any wiki pages were created before Phase 1 (via regular ingestion), add the new standard fields (`requires`, `informs`, `valid_from`, `valid_until`, `traits`) to their frontmatter with empty defaults
- [x] 13. Update `wiki/overview.md` to reflect the novel-author wiki extension capabilities

### Tools Update

- [x] 14. Update `tools/build_graph.py` to extract `requires:`/`informs:` relationships as edges (in addition to `[[wikilinks]]`)
- [x] 15. Update `tools/lint.py` to include novel-specific validation checks

### Final Verification

- [x] 16. Run `/wiki-lint` and verify all novel-specific checks pass
- [x] 17. Run `/wiki-graph` and verify the knowledge graph includes `requires:`/`informs:` edges
- [x] 18. Run `/wiki-ingest` on one raw file and verify it creates both generic (source, entity, concept) and novel-specific (character, location, conflict, theme) pages
- [x] 19. Verify the session-start protocol works end-to-end: CLAUDE.md → todo/README.md → meta/README.md → active phase

### Graph-Erweiterung

- [x] 20. Erweitere `tools/build_graph.py` um `requires:`/`informs:` Kanten-Extraktion aus Frontmatter (zusätzlich zu [[wikilinks]]). Neue Edge-Types: `REQUIRES` und `INFORMS` mit eigenen Farben.
- [x] 21. Füge die vier Oberschichten als Cluster-Gruppierung im Graph hinzu (Knowledge=grün, Narrative=blau, ReaderState=gelb, Meta=grau)

### Deterministische Lint-Integration

- [x] 22. Integriere `tools/lint_deterministic.py` (aus Phase 2) in den wiki-lint Workflow: Erst deterministische Checks (schnell, kein API), dann semantische Checks (API). Deterministische Fehler werden sofort reportet, semantische nur bei Bedarf.
- [x] 23. Ergänze wiki-lint um folgende Checks aus der Oberschicht-Architektur: Knowledge-Layer-Seiten dürfen keine `manuscript_status` oder `beat_number` Felder haben; Narrative-Layer-Seiten müssen `chapter_ref` haben.

### Ingest-Erweiterung für Oberschichten

- [x] 24. Passe `tools/ingest.py` an: Nach dem Erstellen neuer Seiten, prüfe ob sie zur richtigen Oberschicht gehören (z.B. ein neues Konzept gehört zu Knowledge, nicht zu Narrative). Warnmeldung wenn unklar.
- [x] 25. Ergänze den Ingest-Workflow um die `processed/`-Verschiebung (falls nicht schon in Phase 0 erledigt — Idempotenz-Check).

---

## Completion Criteria

- CLAUDE.md fully updated with all novel-specific extensions
- AGENTS.md and GEMINI.md updated with appropriate simplification levels
- All 15 page types documented in CLAUDE.md
- All 13 new directories documented in CLAUDE.md
- Extended ingest, lint, and graph workflows implemented
- At least one end-to-end test (ingest → lint → graph) passes
- Cross-agent schema consistency verified
- `tools/build_graph.py` shows Oberschicht clusters and REQUIRES/INFORMS edges
- `tools/lint_deterministic.py` integrated into wiki-lint workflow

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 4 to `complete`. The extension is ready for production use.
