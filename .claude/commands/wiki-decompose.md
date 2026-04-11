---
name: wiki-decompose
description: per-file planning skill
---

Trigger: "decompose raw/foo.md" or before any interactive ingest session
Runs `tools/decompose.py {file}` and presents the plan to the user.
The decompose output is a FULL inventory — all entity counts must be honored during ingest.
Plan shows: layers touched, known vs. new entities, qmd search commands to run.
User reviews/edits the plan interactively.
Approved plan saved to `log/{branch}/{session}/plan.md`
If the plan contains > 10 entities, add a BATCH MODE flag to the plan file.
SPARK-influenced: asks "what in this file's framing could be wrong or misleading?"
Output: a validated per-file ingest plan, ready for `/wiki-ingest` execution.
