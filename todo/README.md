# Development Roadmap — Novel-Author Wiki Extension

## Phase Status

| Phase | Folder | Status | Description |
|-------|--------|--------|-------------|
| 0 | `phase-0-cleanup/` | `complete` | Infrastruktur: Ingest-Queue-Migration, Wiki-Oberschichten, Progressive Disclosure |
| 1 | `phase-1-schema/` | `complete` | Wiki schema extension: page types, directories, frontmatter, seed templates, folder READMEs |
| 2 | `phase-2-navigation/` | `complete` | Navigation, dependencies, temporal filtering, deterministic lint rules, staleness checks |
| 3 | `phase-3-workflows/` | `complete` | Workflows, slash commands, discovery/validation hooks, SKILL.md migration |
| 4 | `phase-4-integration/` | `complete` | CLAUDE.md integration, graph extension, deterministic lint, ingest updates |
| 5 | `phase-5-writing-pipeline/` | `active` | Writing pipeline: beats, outlines, manuscripts, 4 new workflows |
| 6 | `phase-6-adaptive-ingest/` | `not-started` | Token-efficient ingest: qmd, decompose script, session logging, CLAUDE/GEMINI split, novel page types |

> **Phase 6 note:** Group A tasks (Foundation) can start immediately in parallel with Phase 1.
> Groups B–D depend on Phase 1 wiki directories existing.

---

## Session Start Protocol

Every session that works on wiki extension implementation:

1. **Read this file** — find the active phase (first phase with status != `complete`)
2. **Read `todo/meta/README.md`** — validation rules, contradiction hierarchy, wiki hygiene (MANDATORY)
3. **Read the active phase's `README.md`** — e.g., `todo/phase-1-schema/README.md`
4. **Continue from the first unchecked task** in that phase

**Do NOT read inactive phase folders.** Load `docs/` specs ONLY when the active task references them.

---

## Universal Rules

These rules apply across ALL phases:

### State Tracking
- Mark tasks `- [x]` **immediately** after completing each one
- Update phase status from `active` to `complete` when ALL tasks in the phase are checked
- Set the next phase from `not-started` to `active` when the previous phase completes
- Only **ONE phase** may be `active` at a time

### Wiki Integrity
- Flag contradictions — **never** silently resolve them (log to `wiki/meta/contradiction-log.md`)
- Archive deprecated content to `wiki/archive/` — **never** delete wiki pages
- Follow the contradiction resolution hierarchy: `rule > source > character > chapter > synthesis`

### Context Discipline
- NEVER read phase folders with status `not-started` or `complete` (unless debugging)
- Load `docs/` specs only when the active task explicitly says to
- Keep implementation focused on the current task — don't speculatively implement future phase work

---

## Reference Specs

Detailed specifications live in `/docs/`. Load them ONLY when the active phase README references them.

| Spec | Contents |
|------|----------|
| `docs/wiki-schema.md` | Page types, frontmatter, templates, traits, temporal fields |
| `docs/navigation-system.md` | Dependency system, traversal rules, temporal filtering, ceilings |
| `docs/agent-workflows.md` | 8 workflows with triggers, context loads, outputs, validation |
| `docs/reader-model.md` | Reader progressive disclosure, terminology ratchet, foreshadowing |
| `docs/dramatica-integration.md` | Dramatica Theory mapping to wiki pages |
| `docs/writing-pipeline.md` | Beats, outlines, manuscripts — the writing pipeline |
| `docs/adaptive-ingest.md` | qmd setup, decompose workflow, session logging, agent personas, CLAUDE/GEMINI split |

---

## Meta-Maintenance

To update the todo folder structure itself (add phases, restructure, update rules), read `todo/meta/README.md`.
