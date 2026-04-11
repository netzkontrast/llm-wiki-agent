# Meta-Learning: Self-Improving Pipeline

**Status:** Idea spec — not yet scheduled for implementation  
**Context:** Extends Phase 6 session logging toward continuous pipeline improvement

This document sketches a concept for using qmd on the `meta` layer itself — treating
the session logs, decisions, and protocols as a searchable knowledge base that guides
future agent behaviour, not just as an audit trail.

---

## The Core Idea

The `wiki/meta/ingest/` directory grows a session log after every ingest run:

```
wiki/meta/ingest/
  {branch}/{timestamp}/
    plan.md       — what the agent planned to do
    findings.md   — what actually happened (surprises, failures, contradictions)
    decisions.md  — architectural choices made mid-session
```

Once qmd indexes this (`qmd collection add wiki/meta/ --name meta`), agents can search
across all past sessions:

```sh
qmd search "character merge conflict" -c meta --files
qmd query  "why did foreshadowing classification fail" -c meta
```

This turns a flat log directory into an institutional memory the agent can query before
starting a new session — without loading every log file into context.

---

## Three Capabilities This Enables

### 1. Pre-session priming

Before processing a new raw file, the orchestrator runs:

```sh
qmd query "ingest issues {topic-keywords}" -c meta --files --min-score 0.35
```

If past sessions flagged recurring problems with similar sources (e.g. "Aegis documents
always misclassify CoherenceField as a character"), the agent sees that before writing
anything. Zero extra LLM cost — pure retrieval.

### 2. `/wiki-consolidate` powered by meta-search

The consolidation skill (Phase 6, C6) already reads `findings.md` files. With qmd:

- Instead of reading every file, it runs targeted queries: "what failed most often?"
- It can cross-reference decisions with protocols: "was this decision consistent with
  the context-ceiling rules in `meta/context-protocol.md`?"
- Output: a ranked list of improvement proposals, each grounded in specific past sessions

### 3. Pipeline self-description

Over time, `wiki/meta/` becomes a compressed record of how the system actually behaves
— not just how it was designed to behave. Discrepancies between `docs/` specs and
`meta/ingest/` findings are surfaced automatically by `/wiki-consolidate`.

This creates a feedback loop:
```
session → findings.md → qmd index → consolidate query → improved docs/ → next session
```

---

## What Would Need to Be Built

| Component | Builds on | Effort estimate |
|---|---|---|
| qmd `meta` collection + embed | Phase 6 A3 (install-qmd.sh) | Trivial — add one line |
| Pre-session meta-query in `/wiki-decompose` | Phase 6 C5 | Small — 3 lines in skill |
| Meta-powered `/wiki-consolidate` | Phase 6 C6 | Medium — replace file-glob with qmd query |
| Structured `findings.md` format (machine-readable) | Phase 6 D3 | Small — add schema |
| Discrepancy detection (docs vs. actual behaviour) | After C6 exists | Medium |

None of this requires new infrastructure — it reuses qmd and the session log format
already defined in Phase 6. The only addition is querying `meta` the same way we
query `knowledge` and `narrative`.

---

## Constraints

- **Meta logs never flow into wiki content.** The `meta` layer is system-only;
  findings never become character pages or source summaries.
- **Consolidation never auto-applies.** All proposed changes from `/wiki-consolidate`
  are presented as diffs for human approval. The system describes what to change;
  a human decides whether to apply it.
- **qmd on meta is read-only for agents.** Agents query and read; they do not modify
  protocols or contradiction logs directly. Only `/wiki-consolidate` (with human approval)
  can propose changes to `docs/` and protocol files.

---

## Relation to the Research Synthesis

This is the tractable, low-cost version of the "Metacognitive Role Asymmetry" and
"Error Persistence" concepts from the architectural research. Rather than building
adversarial multi-agent critique loops (which require multiple LLM calls per ingest),
we achieve a similar feedback effect through:

1. Structured logging → machine-readable `findings.md`
2. qmd search → retrieval without context loading
3. `/wiki-consolidate` → periodic human-reviewed improvement

The result is self-improvement grounded in actual session data, not theoretical entropy
thresholds. Implementation follows naturally after Phase 6 is complete.
