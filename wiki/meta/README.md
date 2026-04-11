# Meta Layer — System Administration

This layer contains all system control documents: session logs, protocols,
contradiction log, and session management infrastructure for adaptive ingest.
Serves as audit trail and agent routing.

**Subdirectories and key files (all live here, not at wiki root):**

| Path | What it contains |
|---|---|
| `archive/` | Deprecated pages — never delete, only archive |
| `ingest/` | Session plans, findings, decisions (Phase 6 session logging) |
| `contradiction-log.md` | All detected contradictions (mandatory format) |
| `temporal-protocol.md` | Algorithm for temporal filtering |
| `context-protocol.md` | Context-ceiling and priority-drop rules |
| `staleness-protocol.md` | Detection of stale `informs:` targets |
| `discovery-protocol.md` | Discovery hook before chapter-writing workflows |
| `validation-protocol.md` | Validation hook after generation steps |

> `syntheses/` (saved query answers) lives in `wiki/knowledge/syntheses/` — not here.

## Mutation rule
Append-only for logs. Protocols are updated when rules change. `archive/` only
grows — never delete. `ingest/` session folders created by `tools/session_init.py`.

## When to load
- At session start (check contradiction-log)
- During wiki-lint workflow
- During conflict escalations
- qmd collection: `meta` — `qmd search "term" -c meta`
- For adaptive pipeline learning, see `docs/meta-learning.md`
