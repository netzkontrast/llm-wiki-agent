# Meta Layer — System-Steuerung

Diese Schicht enthält alle systemischen Steuerungsdokumente: Logs, Protokolle,
Contradiction-Log, Indexierungshilfen. Sie dient als Audit-Trail und Agent-Routing.

## Zugehörige Verzeichnisse und Dateien
- [../meta/](../meta/) — Contradiction-Log, temporale und staleness Protokolle
- [../archive/](../archive/) — Archivierte (nie gelöschte) veraltete Wiki-Seiten
- [../syntheses/](../syntheses/) — Gespeicherte Query-Antworten

## Schlüsseldokumente
- `contradiction-log.md` — Alle erkannten Widersprüche (Pflichtformat)
- `temporal-protocol.md` — Algorithmus für zeitliche Filterung
- `context-protocol.md` — Context-Ceiling und Priority-Drop Regeln
- `staleness-protocol.md` — Erkennung veralteter `informs:`-Targets
- `discovery-protocol.md` — Discovery-Hook vor chapter-writing Workflows
- `validation-protocol.md` — Validation-Hook nach Generierungen

## Mutations-Regel
Append-only für Logs. Protokolle werden aktualisiert wenn Regeln sich ändern.
Archiv-Verzeichnis nur erweitern — niemals löschen.

## Wann laden?
- Beim session-start (contradiction-log prüfen)
- Beim wiki-lint Workflow
- Bei Konflikt-Eskalationen
