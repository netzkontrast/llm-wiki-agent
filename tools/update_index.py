import json

def main():
    index_path = "wiki/index.md"
    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open("locations.json", "r", encoding="utf-8") as f:
        locations = json.load(f)

    new_lines = []

    # We will insert concepts under "### Concepts" and locations under "### Locations"

    concept_link = "- [PsychologicalLandscapes](knowledge/concepts/PsychologicalLandscapes.md) — worldbuilding, did\n"

    location_links = []
    for loc in locations:
        if loc['name'] not in ['LogosPrime']:
            link = f"- [{loc['name']}](narrative/locations/{loc['name']}.md) — {loc['title']}\n"
            location_links.append(link)

    for i, line in enumerate(lines):
        new_lines.append(line)
        if line.strip() == "### Concepts":
            new_lines.append(concept_link)
        if line.strip() == "### Locations":
            new_lines.extend(location_links)

    with open(index_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("Updated index.md with new links.")

if __name__ == "__main__":
    main()
