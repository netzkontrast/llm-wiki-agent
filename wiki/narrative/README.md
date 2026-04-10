# Narrative Layer — Plot-Zustände

Diese Schicht enthält alle durch den Schreibprozess mutierten Plot-Zustände.
Jede Änderung im Erzählverlauf schlägt sich hier nieder — nicht im Knowledge Layer.

## Zugehörige Verzeichnisse
- [../chapters/](../chapters/) — Kapitel-Spezifikationen (POV, Timeline, Constraints)
- [../outlines/](../outlines/) — Strukturelle Kapitelplanung (Beat-Sequenzen)
- [../beats/](../beats/) — Atomare Szenenmomente mit Spannung und Foreshadowing
- [../manuscripts/](../manuscripts/) — Ausgeschriebene Prosa-Entwürfe
- [../conflicts/](../conflicts/) — Interne, externe und thematische Konflikte
- [../arcs/](../arcs/) — Charakter- und Plot-Transformationsbögen
- [../themes/](../themes/) — Thematische Fäden und Motive
- [../dramatica/](../dramatica/) — Dramatica Theory Story-Punkte und Throughlines

## Mutations-Regel
Mutiert durch Schreibprozesse. Jeder Beat erzeugt potentiell ein Delta. Änderungen
werden über `informs:`-Ketten in abhängige Seiten propagiert. Immer `last_updated`
aktualisieren nach Änderungen.

## Wann laden?
- Beim chapter-writing Workflow (chapter, outline, beats, manuscript)
- Beim conflict-resolution Workflow
- Beim arc-tracking Workflow
