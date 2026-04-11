import os

def main():
    filepath = "wiki/knowledge/concepts/PsychologicalLandscapes.md"
    if not os.path.exists(filepath):
        content = """---
title: Psychological Landscapes
type: concept
tags: [concept, worldbuilding, did]
sources: [umfassendes-lokalitaten-konzept]
requires: []
informs: []
---

# Psychological Landscapes

Die vier Kern-Welten (KW1-4) des Romans fungieren als Externalisierungen der Psyche des Protagonisten Kael. Sie sind nicht nur passive Hintergründe, sondern aktive Spiegel und Manifestationen seiner inneren Zustände, seiner dissoziativen Identitätsstruktur (DID) und der darin agierenden Alter-Persönlichkeiten.
"""
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(content)
        print(f"Created PsychologicalLandscapes.md")
    else:
        print("PsychologicalLandscapes.md already exists.")

if __name__ == "__main__":
    main()
