#!/usr/bin/env python3
"""
Build the knowledge graph from the wiki.

Usage:
    python tools/build_graph.py               # full rebuild
    python tools/build_graph.py --no-infer    # skip semantic inference (faster)
    python tools/build_graph.py --open        # open graph.html in browser after build

Outputs:
    graph/graph.json    — node/edge data (cached by SHA256)
    graph/graph.html    — interactive vis.js visualization

Edge types:
    EXTRACTED   — explicit [[wikilink]] in a page
    INFERRED    — Claude-detected implicit relationship
    AMBIGUOUS   — low-confidence inferred relationship
"""

import re
import json
import hashlib
import argparse
import webbrowser
from pathlib import Path
from datetime import date

try:
    import networkx as nx
    from networkx.algorithms import community as nx_community
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("Warning: networkx not installed. Community detection disabled. Run: pip install networkx")

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
GRAPH_DIR = REPO_ROOT / "graph"
GRAPH_JSON = GRAPH_DIR / "graph.json"
GRAPH_HTML = GRAPH_DIR / "graph.html"
CACHE_FILE = GRAPH_DIR / ".cache.json"
LOG_FILE = WIKI_DIR / "log.md"
SCHEMA_FILE = REPO_ROOT / "CLAUDE.md"

# Node type → color mapping
TYPE_COLORS = {
    "source": "#4CAF50",
    "entity": "#2196F3",
    "concept": "#FF9800",
    "synthesis": "#9C27B0",
    "unknown": "#9E9E9E",
}

EDGE_COLORS = {
    "EXTRACTED": "#555555",
    "INFERRED": "#FF5722",
    "AMBIGUOUS": "#BDBDBD",
}


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "lint-report.md")]


def extract_wikilinks(content: str) -> list[str]:
    return list(set(re.findall(r'\[\[([^\]]+)\]\]', content)))


def extract_yaml_frontmatter_list(content: str, field: str) -> list[str]:
    match = re.search(rf'^{field}:\s*\[(.*?)\]', content, re.MULTILINE)
    if not match: return []
    inner = match.group(1).strip()
    if not inner: return []
    return [item.strip().strip('"\'').split('/')[-1] for item in inner.split(',')]
def extract_frontmatter(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    yaml_str = match.group(1)
    data = {}
    for line in yaml_str.split('\n'):
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        if val.startswith('[') and val.endswith(']'):
            inner = val[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [item.strip().strip('"\'') for item in inner.split(',')]
        else:
            data[key] = val
    return data


def extract_frontmatter_type(content: str) -> str:
    match = re.search(r'^type:\s*(\S+)', content, re.MULTILINE)
    return match.group(1).strip('"\'') if match else "unknown"


def page_id(path: Path) -> str:
    return path.relative_to(WIKI_DIR).as_posix().replace(".md", "")


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache: dict):
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def build_nodes(pages: list[Path]) -> list[dict]:
    nodes = []
    for p in pages:
        content = read_file(p)
        node_type = extract_frontmatter_type(content)
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
        label = title_match.group(1).strip() if title_match else p.stem
        nodes.append({
            "id": page_id(p),
            "label": label,
            "type": node_type,
            "color": TYPE_COLORS.get(node_type, TYPE_COLORS["unknown"]),
            "path": str(p.relative_to(REPO_ROOT)),
        })
    return nodes


def build_extracted_edges(pages: list[Path]) -> list[dict]:
    """Pass 1: deterministic wikilink edges."""
    # Build a map from stem (lower) -> page_id for resolution
    stem_map = {p.stem.lower(): page_id(p) for p in pages}
    edges = []
    seen = set()
    for p in pages:
        content = read_file(p)
        src = page_id(p)
        for link in extract_wikilinks(content):
            target = stem_map.get(link.lower())
            if target and target != src:
                key = (src, target)
                if key not in seen:
                    seen.add(key)
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "WIKILINK",
                        "color": EDGE_COLORS["EXTRACTED"],
                        "confidence": 1.0,
                    })

        fm = extract_frontmatter(content)
        if fm:
            for req in fm.get("requires", []):
                clean_req = req.split('/')[-1]
                target = stem_map.get(clean_req.lower())
                if target and target != src:
                    key = f"REQUIRES_{src}_{target}"
                    if key not in seen:
                        seen.add(key)
                        edges.append({
                            "from": src,
                            "to": target,
                            "type": "REQUIRES",
                            "color": "#FF9800",
                            "confidence": 1.0,
                        })
            for inf in fm.get("informs", []):
                clean_inf = inf.split('/')[-1]
                target = stem_map.get(clean_inf.lower())
                if target and target != src:
                    key = f"INFORMS_{src}_{target}"
                    if key not in seen:
                        seen.add(key)
                        edges.append({
                            "from": src,
                            "to": target,
                            "type": "INFORMS",
                            "color": "#2196F3",
                            "confidence": 1.0,
                        })
        # Extract requires edges
        for req in extract_yaml_frontmatter_list(content, 'requires'):
            target = stem_map.get(req.lower())
            if target:
                key = f"{src}->{target}"
                if key not in seen:
                    seen.add(key)
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "REQUIRES",
                        "color": "#4CAF50",
                        "confidence": 1.0,
                    })

        # Extract informs edges
        for inf in extract_yaml_frontmatter_list(content, 'informs'):
            target = stem_map.get(inf.lower())
            if target:
                key = f"{src}->{target}"
                if key not in seen:
                    seen.add(key)
                    edges.append({
                        "from": src,
                        "to": target,
                        "type": "INFORMS",
                        "color": "#2196F3",
                        "confidence": 1.0,
                    })
    return edges



def detect_communities(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    """Assign community IDs to nodes using Louvain algorithm."""
    if not HAS_NETWORKX:
        return {}

    G = nx.Graph()
    for n in nodes:
        G.add_node(n["id"])
    for e in edges:
        G.add_edge(e["from"], e["to"])

    if G.number_of_edges() == 0:
        return {}

    try:
        communities = nx_community.louvain_communities(G, seed=42)
        node_to_community = {}
        for i, comm in enumerate(communities):
            for node in comm:
                node_to_community[node] = i
        return node_to_community
    except Exception:
        return {}


COMMUNITY_COLORS = [
    "#E91E63", "#00BCD4", "#8BC34A", "#FF5722", "#673AB7",
    "#FFC107", "#009688", "#F44336", "#3F51B5", "#CDDC39",
]


def render_html(nodes: list[dict], edges: list[dict]) -> str:
    """Generate self-contained vis.js HTML."""
    nodes_json = json.dumps(nodes, indent=2)
    edges_json = json.dumps(edges, indent=2)

    legend_items = "".join(
        f'<span style="background:{color};padding:3px 8px;margin:2px;border-radius:3px;font-size:12px">{t}</span>'
        for t, color in TYPE_COLORS.items() if t != "unknown"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>LLM Wiki — Knowledge Graph</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  body {{ margin: 0; background: #1a1a2e; font-family: sans-serif; color: #eee; }}
  #graph {{ width: 100vw; height: 100vh; }}
  #controls {{
    position: fixed; top: 10px; left: 10px; background: rgba(0,0,0,0.7);
    padding: 12px; border-radius: 8px; z-index: 10; max-width: 260px;
  }}
  #controls h3 {{ margin: 0 0 8px; font-size: 14px; }}
  #search {{ width: 100%; padding: 4px; margin-bottom: 8px; background: #333; color: #eee; border: 1px solid #555; border-radius: 4px; }}
  #info {{
    position: fixed; bottom: 10px; left: 10px; background: rgba(0,0,0,0.8);
    padding: 12px; border-radius: 8px; z-index: 10; max-width: 320px;
    display: none;
  }}
  #stats {{ position: fixed; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 8px; font-size: 12px; }}
</style>
</head>
<body>
<div id="controls">
  <h3>LLM Wiki Graph</h3>
  <input id="search" type="text" placeholder="Search nodes..." oninput="searchNodes(this.value)">
  <div>{legend_items}</div>
  <div style="margin-top:8px;font-size:11px;color:#aaa">
    <span style="background:#555;padding:2px 6px;border-radius:3px;margin-right:4px">──</span> Explicit link<br>
    <span style="background:#FF5722;padding:2px 6px;border-radius:3px;margin-right:4px">──</span> Inferred
  </div>
</div>
<div id="graph"></div>
<div id="info">
  <b id="info-title"></b><br>
  <span id="info-type" style="font-size:12px;color:#aaa"></span><br>
  <span id="info-path" style="font-size:11px;color:#666"></span>
</div>
<div id="stats"></div>
<script>
const nodes = new vis.DataSet({nodes_json});
const edges = new vis.DataSet({edges_json});

const container = document.getElementById("graph");
const network = new vis.Network(container, {{ nodes, edges }}, {{
  nodes: {{
    shape: "dot",
    size: 12,
    font: {{ color: "#eee", size: 13 }},
    borderWidth: 2,
  }},
  edges: {{
    width: 1.2,
    smooth: {{ type: "continuous" }},
    arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }},
  }},
  physics: {{
    stabilization: {{ iterations: 150 }},
    barnesHut: {{ gravitationalConstant: -8000, springLength: 120 }},
  }},
  interaction: {{ hover: true, tooltipDelay: 200 }},
}});

network.on("click", params => {{
  if (params.nodes.length > 0) {{
    const node = nodes.get(params.nodes[0]);
    document.getElementById("info").style.display = "block";
    document.getElementById("info-title").textContent = node.label;
    document.getElementById("info-type").textContent = node.type;
    document.getElementById("info-path").textContent = node.path;
  }} else {{
    document.getElementById("info").style.display = "none";
  }}
}});

document.getElementById("stats").textContent =
  `${{nodes.length}} nodes · ${{edges.length}} edges`;

function searchNodes(q) {{
  const lower = q.toLowerCase();
  nodes.forEach(n => {{
    nodes.update({{ id: n.id, opacity: (!q || n.label.toLowerCase().includes(lower)) ? 1 : 0.15 }});
  }});
}}
</script>
</body>
</html>"""


def append_log(entry: str):
    log_path = WIKI_DIR / "log.md"
    existing = read_file(log_path)
    log_path.write_text(entry.strip() + "\n\n" + existing, encoding="utf-8")


def build_graph(infer: bool = True, open_browser: bool = False):
    pages = all_wiki_pages()
    today = date.today().isoformat()

    if not pages:
        print("Wiki is empty. Ingest some sources first.")
        return

    print(f"Building graph from {len(pages)} wiki pages...")
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    cache = load_cache()

    # Pass 1: extracted edges
    print("  Pass 1: extracting wikilinks...")
    nodes = build_nodes(pages)
    edges = build_extracted_edges(pages)
    print(f"  → {len(edges)} extracted edges")

    # Pass 2: inferred edges (now disabled or handled differently)
    if infer:
        print("  Pass 2: semantic inference requires LLM agent. Skipping pure-python inference.")

    # Layer clustering
    print("  Assigning nodes to layer clusters...")
    LAYER_COLORS = {
        "knowledge": "#4CAF50",    # green
        "narrative": "#2196F3",    # blue
        "reader_state": "#FFEB3B", # yellow
        "meta": "#9E9E9E",         # gray
    }

    for node in nodes:
        path_str = node["path"]
        layer = path_str.split("/")[1] if path_str.startswith("wiki/") and len(path_str.split("/")) > 1 else None
        if layer in LAYER_COLORS:
            node["color"] = LAYER_COLORS[layer]
            node["group"] = layer
        else:
            node["group"] = "other"

    # Save graph.json
    graph_data = {"nodes": nodes, "edges": edges, "built": today}
    GRAPH_JSON.write_text(json.dumps(graph_data, indent=2))
    print(f"  saved: graph/graph.json  ({len(nodes)} nodes, {len(edges)} edges)")

    # Save graph.html
    html = render_html(nodes, edges)
    GRAPH_HTML.write_text(html)
    print(f"  saved: graph/graph.html")

    append_log(f"## [{today}] graph | Knowledge graph rebuilt\n\n{len(nodes)} nodes, {len(edges)} edges ({len([e for e in edges if e['type']=='EXTRACTED'])} extracted, {len([e for e in edges if e['type']=='INFERRED'])} inferred).")

    if open_browser:
        webbrowser.open(f"file://{GRAPH_HTML.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build LLM Wiki knowledge graph")
    parser.add_argument("--infer", action="store_true", help="Run semantic inference (requires agent)")
    parser.add_argument("--open", action="store_true", help="Open graph.html in browser")
    args = parser.parse_args()
    build_graph(infer=args.infer, open_browser=args.open)
