# Phase 3: Agent Workflows & Slash Commands

**Status:** `not-started`
**Prerequisites:** Phase 2 complete
**Spec references:** `docs/agent-workflows.md`, `docs/reader-model.md`, `docs/dramatica-integration.md`

## Purpose

Implement the 8 novel-specific agent workflows as slash commands, with trigger patterns, context-loading rules, output specs, and validation steps. Extend the existing ingest workflow for novel-specific page types.

---

## Tasks

### Slash Command Files

Create new command definitions in `.claude/commands/`. Each file should follow the pattern of existing commands (brief summary, usage, reference to workflow spec).

- [ ] 1. Create `.claude/commands/wiki-chapter.md` — triggers: "write/draft/outline/continue chapter N". References chapter-writing workflow in `docs/agent-workflows.md`.
- [ ] 2. Create `.claude/commands/wiki-character.md` — triggers: "develop/update/profile character X". References character-dev workflow.
- [ ] 3. Create `.claude/commands/wiki-worldbuild.md` — triggers: "build/develop/define location or rule X". References world-building workflow.
- [ ] 4. Create `.claude/commands/wiki-timeline.md` — triggers: "timeline check/view/edit". References timeline-related operations.
- [ ] 5. Create `.claude/commands/wiki-conflict.md` — triggers: "analyze/resolve/develop conflict X". References conflict-resolution workflow.
- [ ] 6. Create `.claude/commands/wiki-reader-model.md` — triggers: "reader state/model for chapter N". References reader-model workflow.
- [ ] 7. Create `.claude/commands/wiki-revise.md` — triggers: "revise chapter(s) N(-M)". References revision workflow.
- [ ] 8. Create `.claude/commands/wiki-lector.md` — triggers: "lector/editorial review chapter N". References lectoring workflow.

### Extended Ingest

- [ ] 9. Update `.claude/commands/wiki-ingest.md` to include steps 10-17 from `docs/agent-workflows.md` "Extended Ingest Workflow" section: create novel-specific pages (character, location, conflict, theme, rule, timeline, foreshadowing) during ingestion.

### Brainstorming

- [ ] 10. Create `.claude/commands/wiki-brainstorm.md` — triggers: "brainstorm/explore/what-if X". References brainstorming workflow.

### Workflow Validation

- [ ] 11. Test chapter-writing workflow: run `/wiki-chapter 1` against the seed pages, verify correct context loading (loads Kael, LogosPrime, KaelVsAegis, IntegrationVsFragmentation, reader-state, constraint_refs)
- [ ] 12. Test character-dev workflow: run `/wiki-character Kael`, verify arc and relationship loading
- [ ] 13. Test reader-model workflow: run `/wiki-reader-model 1`, verify terminology_permitted ratchet and foreshadowing tracking
- [ ] 14. Verify temporal filtering in chapter workflow: ensure Kael.md loads but Kael-post-frag.md does not when working on chapter 1

### Discovery & Validation Hooks

- [ ] 15. Dokumentiere den Discovery-Hook-Mechanismus in `wiki/meta/discovery-protocol.md`: Vor jedem chapter-writing Workflow extrahiert der Agent die `characters:`, `locations:`, `conflicts:` und `constraint_refs:` aus dem Chapter-Frontmatter und lädt NUR diese Seiten aus wiki/knowledge/ — nicht den gesamten Kontext.
- [ ] 16. Dokumentiere den Validation-Hook-Mechanismus in `wiki/meta/validation-protocol.md`: Nach jeder Generierung prüft der Agent: (a) alle constraint_refs eingehalten, (b) terminology_permitted nicht verletzt, (c) max_new_concepts nicht überschritten. Ergebnis wird in wiki/meta/log.md protokolliert.
- [ ] 17. Integriere beide Hooks als explizite Schritte im `chapter-writing` Workflow in `.claude/commands/wiki-chapter.md`

### SKILL.md Migration (optional, Vorbereitung)

- [ ] 18. Erstelle eine Referenz-SKILL.md für den wiki-ingest Workflow als Proof-of-Concept: YAML-Frontmatter mit name, description (imperativ, intent-fokussiert), version, triggers. Body ≤100 Zeilen. Lege sie in `.claude/commands/wiki-ingest/SKILL.md` ab (Unterverzeichnis statt flache Datei).
- [ ] 19. Dokumentiere in `todo/meta/README.md` das SKILL.md Format als empfohlenen Standard für neue Workflows

---

## Completion Criteria

- 9 new slash command files in `.claude/commands/` (8 novel-specific + 1 brainstorm)
- `wiki-ingest.md` updated with extended steps
- At least 3 workflows manually tested against seed pages
- Temporal filtering verified in at least 1 workflow
- All command files follow existing command format conventions
- `wiki/meta/discovery-protocol.md` and `wiki/meta/validation-protocol.md` exist
- Both hooks integrated into `wiki-chapter.md`

When all tasks are checked, update the phase table in `todo/README.md`: set Phase 3 to `complete`, Phase 4 to `active`.
