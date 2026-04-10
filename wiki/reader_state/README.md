# Reader State Layer — Leser-Wissen

Diese Schicht modelliert den Wissensstand des Lesers an jedem Punkt der Erzählung.
Sie akkumuliert monoton — Wissen wird hinzugefügt, niemals gelöscht (Terminology-Ratchet).

## Zugehörige Verzeichnisse
- [../reader-model/](../reader-model/) — Per-Kapitel Leser-Wissensstände
- [../foreshadowing/](../foreshadowing/) — Foreshadowing-Stränge: planted → reinforced → resolved

## Mutations-Regel
Akkumuliert monoton. `terminology_permitted` ist ein One-Way Ratchet — einmal
freigeschaltete Begriffe können nicht wieder entfernt werden. Neue Einträge werden
nach jedem Kapitel hinzugefügt; bestehende Einträge niemals gelöscht.

## Wann laden?
- Beim manuscript-drafting Workflow (als Constraint-Check)
- Beim reader-model Workflow
- Beim wiki-lint Workflow (Terminology-Ratchet-Validierung)
