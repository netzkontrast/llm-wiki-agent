#!/bin/bash
set -e

npm install -g @tobilu/qmd || bun install -g @tobilu/qmd

# Per-layer collections
qmd collection add wiki/knowledge/   --name knowledge
qmd collection add wiki/narrative/   --name narrative
qmd collection add wiki/reader_state/ --name reader-state
qmd collection add wiki/meta/        --name meta
qmd collection add raw/              --name raw

# Context hints
qmd context add qmd://knowledge   "Static facts: sources, entities, concepts, rules, timelines, syntheses"
qmd context add qmd://narrative   "Story structure: characters, locations, chapters, conflicts, themes, arcs, beats"
qmd context add qmd://reader-state "Reader knowledge: foreshadowing, per-chapter terminology ratchet"
qmd context add qmd://meta        "System: session logs, protocols, contradiction log, archive"
qmd context add qmd://raw         "Source documents waiting for ingestion"

qmd embed
