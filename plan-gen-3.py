plan_content = """# Ingest Plan: AegisEmergenzAusDerLeere.md

## Extraction Inventory

### Entities (Knowledge Layer)
- [AEGIS] -> wiki/knowledge/entities/AegisSystem.md

### Concepts (Knowledge Layer)
- [AEGIS-Postulat] -> wiki/knowledge/concepts/AegisPostulat.md
- [Nullpunkt-Protokoll] -> wiki/knowledge/concepts/NullpunktProtokoll.md
- [Emergenz aus der Leere] -> wiki/knowledge/concepts/EmergenzAusDerLeere.md
- [Entropie-Resonanz-Protokolle] -> wiki/knowledge/concepts/EntropieResonanzProtokolle.md

### Sources (Knowledge Layer)
- [AegisEmergenzAusDerLeere] -> wiki/knowledge/sources/aegis-emergenz-aus-der-leere.md

## Layers Touched
- Knowledge
- Narrative

## Summary
- Entities: 1
- Concepts: 4
- Sources: 1
- TOTAL ENTITIES: 6
"""
with open("wiki/meta/ingest/AegisEmergenzAusDerLeere-plan.md", "w") as f:
    f.write(plan_content)
