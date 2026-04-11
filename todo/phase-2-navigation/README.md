# Phase 2: Navigation & Dependency System

**Status:** `complete`
**Prerequisites:** Phase 1 complete
**Spec references:** `docs/navigation-system.md`, `docs/wiki-schema.md`

## Purpose

Implement the dependency traversal system, temporal filtering protocol, context ceilings, and staleness detection. Verify that the seed pages from Phase 1 form a traversable dependency graph.

---

## Tasks

### Dependency Validation

- [x] 1. Write a lint rule (extend `wiki-lint` or create a standalone check) that verifies: every slug in `requires:` and `informs:` across all wiki pages resolves to an existing page. Run it against the seed pages from Phase 1.
- [x] 2. Write a lint rule that verifies: every `valid_from`/`valid_until` reference points to a timeline-event page with `is_boundary: true`. Run against seed pages.
- [x] 3. Write a lint rule that verifies: `terminology_permitted` in each reader-state is a superset of the previous chapter's. Run against seed pages.

### Temporal Filtering

- [x] 4. Document the temporal resolution algorithm as an executable checklist in `wiki/meta/temporal-protocol.md` — agents follow this when loading pages in chapter context. Reference `docs/navigation-system.md` section "Temporal Filtering" for the spec.
- [x] 5. Test temporal filtering manually: given chapter-01's `timeline_start: 001-story-begins`, verify that `wiki/characters/Kael.md` (valid_until: `010-fragmentation-revealed`) loads correctly (it should, since chapter 1 is before event 10).
- [x] 6. Create a second Kael page or section (`wiki/characters/Kael-post-frag.md`) with `valid_from: 010-fragmentation-revealed` to test temporal sibling resolution.

### Context Ceiling Protocol

- [x] 7. Document the context-ceiling and priority-drop protocol as an executable checklist in `wiki/meta/context-protocol.md` — agents follow this to enforce page limits per workflow. Reference `docs/navigation-system.md` ceiling table.

### Staleness Detection

- [x] 8. Document the staleness detection protocol in `wiki/meta/staleness-protocol.md` — how to check `informs:` targets for stale `last_updated` dates. Reference `docs/navigation-system.md` section "Staleness Detection".
- [x] 9. Run a staleness check against the seed pages to verify the protocol works.

### Graph Integration

- [x] 10. Verify that `requires:`/`informs:` edges would appear in the knowledge graph. Update `tools/build_graph.py` or document how these edges should be extracted alongside `[[wikilinks]]`.

### Deterministische Lint-Rules (kein LLM nötig)

- [x] 11. Lint-Rule: `constraint_refs` Validierung — jeder Slug in einem chapter's `constraint_refs:` muss auf eine existierende Datei in `wiki/rules/` zeigen
- [x] 12. Lint-Rule: `characters:` Validierung — jeder Slug in einem chapter's `characters:` muss eine Datei in `wiki/characters/` haben
- [x] 13. Lint-Rule: Foreshadowing-Vollständigkeit — jede Foreshadowing-Seite mit `status: planted` und `planted_chapter` < letztes Kapitel muss entweder `resolved_chapter` haben oder als "intentionally unresolved" markiert sein
- [x] 14. Lint-Rule: `valid_from`/`valid_until` Konsistenz — referenzierte Timeline-Events müssen `is_boundary: true` haben
- [x] 15. Sammle alle deterministischen Lint-Rules in einem eigenständigen Script `tools/lint_deterministic.py` (kein API-Key nötig, rein Dateisystem + Regex/YAML-Parsing)

### Staleness-Check als Script

- [x] 16. Implementiere `tools/check_staleness.py`: Vergleiche `last_updated` Felder über `informs:`-Ketten. Output: Liste staler Seiten mit Kette (A informiert B, A neuer als B). Kein API-Key nötig.

### Oberschicht-Routing-Validierung

- [x] 17. Lint-Rule: Jede Wiki-Seite muss genau einer der vier Oberschichten zuordenbar sein (basierend auf ihrem Verzeichnis). Warnung wenn eine Seite in einem Verzeichnis liegt, das keiner Oberschicht zugeordnet ist.

---

## Completion Criteria

- Lint rules exist for: reference resolution, temporal validity, terminology ratchet
- Three protocol docs exist in `wiki/meta/`: temporal, context-ceiling, staleness
- Temporal filtering works correctly with seed pages (manual test)
- Temporal sibling resolution demonstrated with Kael / Kael-post-frag
- All seed pages pass all lint rules
- `tools/lint_deterministic.py` exists and covers all deterministic checks
- `tools/check_staleness.py` exists and traverses `informs:` chains
- Oberschicht-Routing-Validierung implementiert

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 2 to `complete`, Phase 3 to `active`.
