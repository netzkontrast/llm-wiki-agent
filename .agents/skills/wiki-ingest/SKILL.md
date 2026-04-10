---
name: wiki-ingest
description: >
  Verarbeitet Rohtexte in atomare semantische Claims und führt einen Ingest in das Dual-State-Wiki durch.
  Use when rohe Quelldokumente oder neue Informations-Chunks in den Kanon aufgenommen werden müssen,
  wobei Widersprüche erkannt und über die MetaCrit-Architektur aufgelöst werden.
  Verwende diesen Skill nicht für das Schreiben von Kapiteln.
version: 1.0.0
license: MIT
---
# Wiki Ingest Workflow

Bevor du eine Datei schreibst, führe aus: python tools/read_lines_fast.py wiki/meta/ingest/plan.md 0 20

1. Planning (Manus-Adaptation): Lese wiki/meta/ingest/plan.md und taxonomies.md ein.
2. Decomposition und Critical Thinking: Zerlege Text in Claims. Challenge Rate Maximization: Widerspricht ein Claim dem Kanon?
3. Semantic Delta: Bei Redundanz verdichten, bei Informationsgewinn > Schwellenwert neue Datei anlegen.
4. MetaCrit Evaluierung: Wenn ein Konflikt zwischen einer neuen Extraktion und dem Kanon entsteht, unterbreche den Schreibvorgang und schreibe den Konflikt formatiert in wiki/meta/ingest/registers/contradictions.md.
5. Das JRE-L Framework für Reader State.
