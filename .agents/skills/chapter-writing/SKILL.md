---
name: chapter-writing
description: >
  Generiert narrative Manuskripte basierend auf Plot-Outlines und Charakter-Zuständen (States).
  Use when ein neues Manuskript-Kapitel verfasst werden soll. Dieser Skill orchestriert das JRE-L Framework
  zur Einhaltung von "Progressive Disclosure" in Bezug auf den simulierten Leser.
  Verwende diesen Skill nicht für den Ingest von Rohtexten.
version: 1.0.0
license: MIT
---
# Chapter Writing Workflow

Bevor du eine Datei schreibst, führe aus: python tools/read_lines_fast.py wiki/meta/ingest/plan.md 0 20

Orchestriert die Pipeline: Outline -> Beat -> Manuscript.
Nutzt K1 Narrative Layer states/ als Startpunkt und generiert Deltas.
