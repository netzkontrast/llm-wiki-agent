---
name: contradiction-check
description: >
  Überprüft semantische Konflikte (Semantic Deltas) zwischen neuen Claims und dem existierenden Kanon.
  Use when ein potenzielles Zeitlinien-Paradoxon, widersprüchliche Fakten oder logische Fehler im Kanon (wiki/knowledge)
  identifiziert werden. Verweigert zerstörende Überschreibungen und lagert Konflikte in contradictions.md aus.
version: 1.0.0
license: MIT
---
# Contradiction Check Workflow

Vergleicht Claims aus neuen Dateien mit dem etablierten K0 Kanon in wiki/knowledge/.
Lagert Widersprüche in wiki/meta/ingest/registers/contradictions.md aus.
