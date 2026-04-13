---
name: wiki-consolidate
description: Executes the following: continuous improvement skill. Use when the user requests wiki-consolidate or related tasks.
---

# wiki-consolidate

Trigger: "consolidate session findings" or run periodically.
Reads all `log/{branch}/*/findings.md` files since last consolidation.
Uses `qmd search -c meta` to find related past decisions and protocols.
Proposes concrete improvements to: `docs/`, `CLAUDE.md`/`GEMINI.md`, wiki READMEs.
Outputs a diff-style proposal; user approves before any file is written.
Never writes wiki content — only improves instructions and navigation.
