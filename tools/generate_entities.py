import json
import os

def main():
    with open("locations.json", "r", encoding="utf-8") as f:
        locations = json.load(f)

    for loc in locations:
        filename = loc['name'] + ".md"
        filepath = os.path.join("wiki/narrative/locations", filename)

        # Check if already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename}, already exists.")
            continue

        content = f"""---
title: {loc['title']}
type: location
tags: [location, worldbuilding]
sources: [umfassendes-lokalitaten-konzept]
requires: []
informs: []
---

# {loc['title']}

{loc['desc']}
"""
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(content)
        print(f"Created {filename}")

if __name__ == "__main__":
    main()
