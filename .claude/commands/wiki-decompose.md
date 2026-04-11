---
name: wiki-decompose
description: per-file planning skill
---

Trigger: "decompose raw/foo.md" or before any interactive ingest session
Runs `tools/decompose.py {file}` and presents the plan to the user.
Plan shows: layers touched, known vs. new entities, qmd search commands to run.
User reviews/edits the plan interactively.
Approved plan saved to `log/{branch}/{session}/plan.md`
SPARK-influenced: asks "what in this file's framing could be wrong or misleading?"
Output: a validated per-file ingest plan, ready for `/wiki-ingest` execution.
