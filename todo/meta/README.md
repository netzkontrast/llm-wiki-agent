# Todo Folder Maintenance

This file governs how the `/todo` folder itself is created, updated, and maintained. Read this file at every session start — it contains validation rules and protocols that apply across ALL phases.

---

## When to Read This File

- **Every session start** (MANDATORY — registered in CLAUDE.md)
- When creating new phases
- When restructuring the todo folder
- When updating universal rules
- During dedicated "todo maintenance" sessions

---

## Session-Start Protocol (Expanded)

1. Read `todo/README.md` — find the active phase
2. Read **this file** (`todo/meta/README.md`) — validation + hygiene rules below
3. Quick check: are any `informs:` chains stale? (grep `informs:` across wiki, compare `last_updated` dates)
4. Read the active phase's `README.md`
5. Continue from the first unchecked task

---

## Validation Rules

Structural invariants the wiki must always satisfy. Check these when modifying wiki content:

1. **Character references:** Every character slug in a chapter's `characters:` field must have a corresponding page in `wiki/characters/`
2. **Informs targets:** Every slug in any page's `informs:` field must resolve to an existing page
3. **Constraint refs:** Every slug in a chapter's `constraint_refs:` must point to a valid rule page in `wiki/rules/`
4. **Foreshadowing completeness:** Every foreshadowing page with `status: planted` must either have a `resolved_chapter` set, or be explicitly flagged as "intentionally unresolved"
5. **Rule compliance:** No page may contradict a rule page it references in `constraint_refs`
6. **Terminology ratchet:** Each reader-state's `terminology_permitted` must be a superset of the previous chapter's `terminology_permitted`
7. **Temporal consistency:** If a page has `valid_from` or `valid_until`, the referenced timeline-event must exist and have `is_boundary: true`

---

## Contradiction Resolution

### Hierarchy (highest authority first)

```
rule pages > source pages > character pages > chapter pages > synthesis pages
```

When two wiki pages disagree:
1. Determine which page type ranks higher in the hierarchy
2. The higher-ranking page is authoritative
3. **Do NOT silently resolve** — log the contradiction
4. Update or flag the lower-ranking page

### Contradiction Log

All contradictions go to `wiki/meta/contradiction-log.md`:

```markdown
## YYYY-MM-DD
- **Conflict:** [page A] says X, [page B] says Y
- **Rule:** [which hierarchy level applies]
- **Status:** open | resolved
- **Resolution:** [what was decided, if resolved]
```

Create this file when the first contradiction is found. It lives in `wiki/meta/` to keep it out of the main index.

---

## Wiki Hygiene

### Folder READMEs (MANDATORY)

Every folder under `wiki/` MUST contain a `README.md` with navigational information:
- **What this folder contains** — page type, naming convention, brief purpose
- **How to find the right page** — listing of all pages in the folder with one-line descriptions
- **How pages relate** — which other folders/page types connect to these pages
- **Temporal note** (if applicable) — whether pages in this folder use `valid_from`/`valid_until`

Update the folder README whenever a page is added, removed, or archived. This is a **mandatory step in every workflow that creates or modifies wiki pages**. The README serves as a local navigation index — agents can read one folder's README instead of scanning all files to find the right page.

```markdown
# [Folder Name]

[1-2 sentence description of what lives here.]

## Pages
- [PageName.md](PageName.md) — one-line description
- [PageName2.md](PageName2.md) — one-line description

## Connections
- Related to: `wiki/[other-folder]/` — how they connect
- Referenced by: `wiki/[other-folder]/` — who links here

## Conventions
- Naming: [convention for this folder]
- Temporal: [yes/no — whether pages use valid_from/valid_until]
```

### Progressive Disclosure via Unterverzeichnisse

Wenn eine Wiki-Seite zu komplex wird (>200 Zeilen) oder mehrere klar trennbare
Aspekte abdeckt, kann sie in ein Unterverzeichnis aufgelöst werden:

Statt:
```
wiki/characters/Kael.md (300 Zeilen, Profile + Psychologie + Voice + Arc)
```

Verwende:
```
wiki/characters/Kael/
  README.md        — Kurzprofil + Navigation (L1: immer laden)
  psychology.md    — Psychologisches Framework (L2: bei character-dev laden)
  voice.md         — Stimmenprofil und Syntax-Patterns (L2: bei manuscript-drafting laden)
  arc-states/      — Temporale Zustände (L3: nur bei spezifischem Kapitelkontext)
    pre-fragmentation.md
    post-fragmentation.md
    integrated.md
```

Die README.md im Unterverzeichnis dient als L1-Discovery-Dokument:
- Maximal 50 Zeilen
- Enthält: Name, Rolle, aktuelle Arc-Phase, Liste der Sub-Dokumente
- Agent lädt die README immer, Sub-Dokumente nur bei Bedarf (Progressive Disclosure)

**Schwellenwerte:**
- >200 Zeilen → Split erwägen
- >2 distinkte Themen → Split empfohlen

### When to Consolidate
- Two pages cover the same entity with <50% distinct content → merge into one
- After merging, update all `[[wikilinks]]` pointing to the removed page

### When to Split
- A page exceeds 200 lines → consider splitting by topic
- A page covers 2+ distinct subjects → split into separate pages

### Archiving (Never Delete)
- **Never delete wiki pages.** Move deprecated content to `wiki/archive/`
- Add a dated reason at the top of the archived page:
  ```
  > **Archived YYYY-MM-DD:** Reason for archival. Superseded by [[NewPage]].
  ```
- Remove the archived page from `wiki/index.md`
- Keep `[[wikilinks]]` to archived pages working (they just point to `archive/`)

### Naming Edge Cases
- Multi-word names: TitleCase without spaces (`MnemosyneArchipelago.md`)
- Acronyms: ALL CAPS (`AEGIS.md`, `TSDP.md`)
- Compound concepts: TitleCase (`DualKernelTheory.md`)
- If unsure, check `docs/wiki-schema.md` naming conventions table

---

## Managing the Todo Folder

### Adding a New Phase

1. Create `todo/phase-N-name/README.md`
2. Add a row to the phase table in `todo/README.md`
3. The new README must include:
   - Phase purpose and scope
   - Prerequisite phases (which must be `complete`)
   - Numbered task list with checkboxes
   - Completion criteria
   - References to relevant `docs/` specs
4. Set status to `not-started`

### Restructuring a Phase

1. Read the target phase README
2. Add/remove/reorder tasks as needed
3. If tasks have been completed, keep them checked — don't remove completed tasks
4. If splitting a phase, create the new phase folder and redistribute tasks

### Updating Universal Rules

1. Edit `todo/README.md` for rules that apply to all phases
2. Edit this file (`todo/meta/README.md`) for validation, contradiction, and hygiene rules
3. Do NOT put universal rules in phase-specific READMEs — that causes duplication

### Keeping Context Clean

- Each phase README is self-contained for its scope
- Phase READMEs must NOT duplicate rules from `todo/README.md` or this file
- Phase READMEs should LINK to `docs/` specs rather than inlining them
- If a spec section exceeds 50 lines, it belongs in `docs/`, not in a phase README

### Session Routing Summary

| Session Type | Read Path |
|--------------|-----------|
| Implementation | `todo/README.md` → `todo/meta/README.md` → active phase README |
| Maintenance | `todo/README.md` → `todo/meta/README.md` (this file) |
| Reference | `docs/README.md` → specific doc |
| Normal wiki work | `CLAUDE.md` (existing workflows) |

## SKILL.md Standard
For agent workflows, it's recommended to place them in a subdirectory named after the workflow and create a `SKILL.md` inside it. The `SKILL.md` file should contain YAML frontmatter with the following keys:
- `name`: The name of the workflow.
- `description`: An imperative, third-person description of the workflow, and intent-focused description of when it should be used.
- `version`: The version of the workflow.
- `triggers`: A list of trigger phrases that should activate the workflow.

The body of the `SKILL.md` should be concise, ideally under 100 lines. See `.claude/commands/wiki-ingest/SKILL.md` for an example.
