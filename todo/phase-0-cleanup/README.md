# Phase 0: Infrastruktur-Bereinigung

**Status:** `complete`
**Prerequisites:** Keine
**Spec reference:** Keine (eigenständig)

## Purpose

Bereinige die Projektstruktur bevor die Novel-Extension implementiert wird.
Entferne veraltete Patterns, etabliere die Ingest-Queue-Mechanik über
Dateisystem statt Checkliste, und lege die vier Wiki-Oberschichten an.

---

## Tasks

### Ingest-Queue-Migration

- [x] 1. Erstelle `processed/` Verzeichnis mit `.gitkeep` und `README.md`
- [x] 2. Entferne den gesamten "Ingestion Queue" Checkbox-Abschnitt aus `CLAUDE.md`
- [x] 3. Ersetze ihn durch die dateisystembasierte Queue-Dokumentation (raw/ → processed/)
- [x] 4. Füge Schritt 10 (mv raw/ → processed/) zum Ingest Workflow in `CLAUDE.md` hinzu
- [x] 5. Aktualisiere `AGENTS.md` mit derselben Queue-Mechanik und Ingest-Schritt
- [x] 6. Aktualisiere `GEMINI.md` mit derselben Queue-Mechanik und Ingest-Schritt
- [x] 7. Aktualisiere das Directory Layout in allen drei Dateien (CLAUDE.md, AGENTS.md, GEMINI.md) um `processed/`

### Wiki-Oberschichten

- [x] 8. Erstelle `wiki/knowledge/` mit README.md (Routing-Dokument für statischen Canon)
- [x] 9. Erstelle `wiki/narrative/` mit README.md (Routing-Dokument für Plot-Zustände)
- [x] 10. Erstelle `wiki/reader_state/` mit README.md (Routing-Dokument für Leser-Wissen)
- [x] 11. Erstelle `wiki/meta/` Verzeichnis falls nicht vorhanden, aktualisiere README.md als Routing-Dokument
- [x] 12. Aktualisiere `CLAUDE.md` Directory Layout um die vier Oberschichten und ihre Zuordnungen

### Progressive-Disclosure-Regel

- [x] 13. Ergänze die "Progressive Disclosure via Unterverzeichnisse"-Regel in `todo/meta/README.md` (Wiki Hygiene Abschnitt)
- [x] 14. Dokumentiere die Schwellenwerte: >200 Zeilen → Split erwägen, >2 distinkte Themen → Split empfohlen

### tools/ingest.py Update

- [x] 15. Erweitere `tools/ingest.py`: nach erfolgreichem Ingest, verschiebe Quelldatei von `raw/` nach `processed/` (os.rename oder shutil.move)
- [x] 16. Füge Error-Handling hinzu: nur verschieben wenn ALLE Schreiboperationen erfolgreich waren

---

## Completion Criteria

- `processed/` existiert mit README.md
- Kein Checkbox-basierter Ingest-Queue mehr in CLAUDE.md/AGENTS.md/GEMINI.md
- Vier Wiki-Oberschichten-Verzeichnisse existieren mit Routing-READMEs
- `tools/ingest.py` verschiebt Dateien nach processed/ nach erfolgreichem Ingest
- Progressive-Disclosure-Regel dokumentiert

Wenn alle Tasks erledigt: Phase 0 → `complete`, Phase 1 → `active`.
