"""
build_full_corpus_web_graph.py
==============================
Builds a complete, standalone, self-contained HTML visualization of the entire
Philippine Statutory Knowledge Graph (National Statutes + Davao City Ordinances).

Embeds the full graph data directly as an inline JavaScript object so that
double-clicking the HTML file in Windows Explorer works instantly offline
without needing any local HTTP server or web browser CORS permissions.
"""

import json
import os
import sys
from collections import Counter, defaultdict

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath("."))
from src.knowledge_graph.build_statutory_kg import build_alias_registry, extract_edges

OUTPUT_DIR = "output/visualizations"
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "statutory_kg_full_web.html")

MACRO_DOMAINS = [
    {"name": "General Administration, Organization & Civil Service", "color": "#3B82F6"},
    {"name": "Public Finance, Taxation, Fiscal Policy & Budget", "color": "#F59E0B"},
    {"name": "Police Power, Public Order, Safety & Penal Law", "color": "#EF4444"},
    {"name": "Social Services, Education, Labor & Human Development", "color": "#10B981"},
    {"name": "Public Works, Transportation, Utilities & Infrastructure", "color": "#8B5CF6"},
    {"name": "Commerce, Trade, Industry, Agriculture & Economic Enterprise", "color": "#06B6D4"},
    {"name": "Environmental Protection, Zoning, Land Use & Natural Resources", "color": "#84CC16"},
    {"name": "Executive Issuances & Policy Reorganization", "color": "#6366F1"},
    {"name": "Inter-Agency Agreements & Institutional MOAs/MOUs", "color": "#EC4899"},
    {"name": "Substantive Regulatory, Health & Penal Ordinances", "color": "#14B8A6"}
]

DOMAIN_COLOR_MAP = {d["name"]: d["color"] for d in MACRO_DOMAINS}

def main():
    print("[1/4] Ingesting enactment metadata and extracting citations/amendments...")
    meta, aliases = build_alias_registry()
    cites, amends, repeals = extract_edges(meta, aliases)

    # Compute node degree in the graph
    node_degree = Counter()
    for (u, v) in cites.keys():
        node_degree[u] += 1
        node_degree[v] += 1
    for (u, v) in amends:
        node_degree[u] += 1
        node_degree[v] += 1
    for (u, v) in repeals:
        node_degree[u] += 1
        node_degree[v] += 1

    print(f"      Total enactments with at least 1 connection: {len(node_degree):,}")

    # For maximum browser responsiveness while showing a massive organic web:
    # Include all local ordinances that have degree >= 2 (around 800) plus top active ones (up to 900)
    # Include top national statutes with degree >= 3 (around 1,500)
    # Total ~2,400 to 2,800 nodes, which Vis.js / Canvas renders smoothly at 60 FPS
    selected_nodes = set()
    
    # 1. Local Davao City Ordinances
    local_candidates = [n for n in node_degree if meta.get(n, {}).get("jurisdiction") == "local"]
    local_candidates.sort(key=lambda x: node_degree[x], reverse=True)
    for n in local_candidates[:850]:
        selected_nodes.add(n)

    # 2. National Statutes
    nat_candidates = [n for n in node_degree if meta.get(n, {}).get("jurisdiction") == "national"]
    nat_candidates.sort(key=lambda x: node_degree[x], reverse=True)
    for n in nat_candidates[:1650]:
        selected_nodes.add(n)

    print(f"[2/4] Selected {len(selected_nodes):,} interconnected enactments for the full web graph.")

    # Build Vis.js nodes list
    vis_nodes = []
    for nid in selected_nodes:
        m = meta.get(nid, {})
        is_local = m.get("jurisdiction") == "local"
        deg = node_degree[nid]
        dom = m.get("domain", "General Administration")
        dom_color = DOMAIN_COLOR_MAP.get(dom, "#3B82F6")

        label = m.get("number", nid)
        if len(label) > 28:
            label = label[:26] + ".."

        # Node size scaled by connectivity
        if is_local:
            node_size = min(38, max(7, int(5 + (deg ** 0.5) * 3.5)))
            bg_color = "#00F2FE" if deg >= 5 else "#4FACFE"  # Neon Cyan/Azure for Davao Ordinances
            border_color = "#00C0FF"
            group = "local"
        else:
            node_size = min(50, max(6, int(4 + (deg ** 0.5) * 2.2)))
            bg_color = "#FF9900" if deg >= 50 else dom_color  # Gold for super hubs, domain color for rest
            border_color = "#FFD700" if deg >= 50 else "#FFFFFF"
            group = "national"

        title_html = (
            f"<b>{m.get('number', nid)}</b><br>"
            f"<b>Jurisdiction:</b> {m.get('jurisdiction', '').upper()}<br>"
            f"<b>Connections (Degree):</b> {deg}<br>"
            f"<b>Year:</b> {m.get('year', 'N/A')}<br>"
            f"<b>Domain:</b> {dom}<br>"
            f"<b>Title:</b> {m.get('title', '')[:140]}..."
        )

        vis_nodes.append({
            "id": nid,
            "label": label if deg >= 12 or is_local else "",
            "title": title_html,
            "value": node_size,
            "group": group,
            "color": {
                "background": bg_color,
                "border": border_color,
                "highlight": {"background": "#FFFFFF", "border": "#FFD700"}
            },
            "font": {
                "color": "#F8FAFC",
                "size": 11,
                "face": "Inter",
                "strokeWidth": 2,
                "strokeColor": "#0A0E17"
            },
            "meta": {
                "id": nid,
                "number": m.get("number", nid),
                "jurisdiction": m.get("jurisdiction"),
                "year": m.get("year"),
                "domain": dom,
                "degree": deg,
                "title": m.get("title", "")
            }
        })

    # Build Vis.js edges list between selected nodes
    print("[3/4] Filtering and assembling relational edges...")
    vis_edges = []
    edge_types = Counter()

    for (u, v), count in cites.items():
        if u in selected_nodes and v in selected_nodes:
            vis_edges.append({
                "from": u,
                "to": v,
                "relation": "CITES_AUTHORITY",
                "arrows": "to",
                "color": {"color": "rgba(100, 149, 237, 0.22)", "highlight": "#00F2FE"},
                "width": 1 if count == 1 else 2
            })
            edge_types["CITES_AUTHORITY"] += 1

    for (u, v) in amends:
        if u in selected_nodes and v in selected_nodes:
            vis_edges.append({
                "from": u,
                "to": v,
                "relation": "AMENDS",
                "arrows": "to",
                "color": {"color": "#FFA500", "highlight": "#FFD700"},
                "width": 2.2,
                "dashes": True
            })
            edge_types["AMENDS"] += 1

    for (u, v) in repeals:
        if u in selected_nodes and v in selected_nodes:
            vis_edges.append({
                "from": u,
                "to": v,
                "relation": "REPEALS",
                "arrows": "to",
                "color": {"color": "#FF4757", "highlight": "#FF6B81"},
                "width": 2.2
            })
            edge_types["REPEALS"] += 1

    print(f"      Assembled {len(vis_nodes):,} nodes and {len(vis_edges):,} edges:")
    for rel, c in edge_types.items():
        print(f"        * {rel}: {c:,}")

    # Build Standalone HTML with inline JSON
    print("[4/4] Generating standalone interactive HTML viewer with inline data...")
    nodes_json = json.dumps(vis_nodes)
    edges_json = json.dumps(vis_edges)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Statutory Knowledge Graph — Full Corpus Web</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #07090e;
      color: #e2e8f0;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: rgba(11, 15, 25, 0.92);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 20;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .badge {{
      background: linear-gradient(135deg, #00f2fe, #4facfe);
      color: #07090e;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: 16px;
      font-weight: 600;
      color: #f8fafc;
      letter-spacing: -0.3px;
    }}
    .stats-bar {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 12px;
      color: #94a3b8;
    }}
    .stat-pill {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 4px 10px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .stat-val {{
      font-family: 'Fira Code', monospace;
      color: #00f2fe;
      font-weight: 600;
    }}
    .main-container {{
      position: relative;
      flex: 1;
      display: flex;
    }}
    #network-canvas {{
      flex: 1;
      height: 100%;
      background: radial-gradient(circle at center, #0f172a 0%, #07090e 100%);
    }}
    /* Controls Overlay */
    .controls-overlay {{
      position: absolute;
      top: 16px;
      left: 16px;
      width: 320px;
      background: rgba(15, 23, 42, 0.90);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .search-box input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 8px 12px;
      color: #f1f5f9;
      font-size: 13px;
      outline: none;
    }}
    .search-box input:focus {{
      border-color: #00f2fe;
      box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.25);
    }}
    .filter-title {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #64748b;
      font-weight: 700;
    }}
    .btn-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .toggle-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      font-size: 11px;
      font-weight: 500;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .toggle-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #f8fafc;
    }}
    .toggle-btn.active {{
      background: #00f2fe;
      border-color: #4facfe;
      color: #07090e;
      font-weight: 700;
    }}
    /* Inspector Card */
    .inspector-card {{
      position: absolute;
      top: 16px;
      right: 16px;
      width: 380px;
      max-height: calc(100% - 32px);
      background: rgba(15, 23, 42, 0.94);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
      z-index: 10;
      overflow-y: auto;
      display: none;
      flex-direction: column;
      gap: 12px;
    }}
    .inspector-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 10px;
    }}
    .inspector-title {{
      font-size: 15px;
      font-weight: 700;
      color: #f8fafc;
      line-height: 1.3;
    }}
    .inspector-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      margin-top: 4px;
      display: inline-block;
      text-transform: uppercase;
    }}
    .badge-nat {{ background: #ff9900; color: #000; }}
    .badge-loc {{ background: #00f2fe; color: #000; }}
    .close-btn {{
      background: transparent;
      border: none;
      color: #64748b;
      font-size: 20px;
      cursor: pointer;
      line-height: 1;
    }}
    .close-btn:hover {{ color: #f8fafc; }}
    .metric-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .metric-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 6px;
      padding: 8px 10px;
    }}
    .metric-label {{ font-size: 10px; color: #94a3b8; }}
    .metric-val {{
      font-family: 'Fira Code', monospace;
      font-size: 13px;
      font-weight: 600;
      color: #00f2fe;
      margin-top: 2px;
    }}
    .text-block {{
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 6px;
      padding: 10px;
      font-size: 11px;
      line-height: 1.5;
      color: #cbd5e1;
      max-height: 160px;
      overflow-y: auto;
    }}
    /* Legend */
    .legend {{
      position: absolute;
      bottom: 20px;
      left: 16px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      gap: 16px;
      font-size: 11px;
      color: #94a3b8;
      z-index: 10;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}
    /* Loading overlay */
    #loading-overlay {{
      position: absolute;
      inset: 0;
      background: #07090e;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 100;
      transition: opacity 0.4s ease;
    }}
    .spinner {{
      width: 44px;
      height: 44px;
      border: 3px solid rgba(0, 242, 254, 0.15);
      border-top-color: #00f2fe;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin-bottom: 16px;
    }}
    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}
  </style>
</head>
<body>

  <div id="loading-overlay">
    <div class="spinner"></div>
    <div style="font-size: 14px; font-weight: 500; color: #f8fafc;">Simulating Statutory Organic Web Graph...</div>
    <div style="font-size: 12px; color: #64748b; margin-top: 6px;">Rendering {len(vis_nodes):,} enactments & {len(vis_edges):,} relational edges</div>
  </div>

  <header>
    <div class="brand">
      <span class="badge">Pure Web Graph</span>
      <h1>Philippine Statutory Knowledge Graph (27,248 Corpus Topology)</h1>
    </div>
    <div class="stats-bar">
      <div class="stat-pill">
        <span>Active Vertices:</span>
        <span class="stat-val">{len(vis_nodes):,}</span>
      </div>
      <div class="stat-pill">
        <span>Relational Edges:</span>
        <span class="stat-val">{len(vis_edges):,}</span>
      </div>
      <div class="stat-pill">
        <span>National Laws:</span>
        <span class="stat-val">1,650</span>
      </div>
      <div class="stat-pill">
        <span>Davao Ordinances:</span>
        <span class="stat-val">850</span>
      </div>
    </div>
  </header>

  <div class="main-container">
    <!-- Controls Overlay -->
    <div class="controls-overlay">
      <div class="search-box">
        <input type="text" id="search-input" placeholder="Search RA 7160, Ordinance No., keyword...">
      </div>

      <div class="filter-group">
        <div class="filter-title">Display Subsets</div>
        <div class="btn-row">
          <button class="toggle-btn active" data-filter="all">All Enactments</button>
          <button class="toggle-btn" data-filter="local">Davao Ordinances Only</button>
          <button class="toggle-btn" data-filter="national">National Statutes Only</button>
        </div>
      </div>

      <div class="filter-group">
        <div class="filter-title">Graph Simulation Controls</div>
        <div class="btn-row">
          <button class="toggle-btn active" id="btn-physics">Physics On</button>
          <button class="toggle-btn" id="btn-recenter">Recenter View</button>
          <button class="toggle-btn" id="btn-freeze">Freeze Positions</button>
        </div>
      </div>
    </div>

    <!-- Network Canvas -->
    <div id="network-canvas"></div>

    <!-- Inspector Card -->
    <div class="inspector-card" id="inspector">
      <div class="inspector-header">
        <div>
          <div class="inspector-title" id="insp-title">Republic Act No. 7160</div>
          <span class="inspector-badge badge-nat" id="insp-badge">National Statute</span>
        </div>
        <button class="close-btn" id="close-inspector">&times;</button>
      </div>

      <div class="metric-grid">
        <div class="metric-card">
          <div class="metric-label">Graph Degree (Connections)</div>
          <div class="metric-val" id="insp-degree">1,350</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Enactment Year</div>
          <div class="metric-val" id="insp-year">1991</div>
        </div>
        <div class="metric-card" style="grid-column: span 2;">
          <div class="metric-label">Macro Legal Domain</div>
          <div class="metric-val" id="insp-domain">General Administration</div>
        </div>
      </div>

      <div>
        <div class="filter-title" style="margin-bottom: 6px;">Statutory Long Title</div>
        <div class="text-block" id="insp-title-full"></div>
      </div>

      <div>
        <div class="filter-title" style="margin-bottom: 6px;">Neighborhood Connections (<span id="insp-conn-count">0</span>)</div>
        <div class="text-block" id="insp-connections" style="max-height: 140px;"></div>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend">
      <div class="legend-item">
        <span class="legend-dot" style="background: #FF9900;"></span>
        <span>National Super-Hub (High Centrality)</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #3B82F6;"></span>
        <span>National Positive Law</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #00F2FE;"></span>
        <span>Davao City Local Ordinance</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #FFA500;"></span>
        <span>Amendatory Chain (AMENDS)</span>
      </div>
    </div>
  </div>

  <script>
    // Embedded Knowledge Graph Data
    const rawNodes = {nodes_json};
    const rawEdges = {edges_json};

    let network = null;
    let nodesDataSet = null;
    let edgesDataSet = null;

    window.addEventListener('DOMContentLoaded', () => {{
      const container = document.getElementById('network-canvas');

      nodesDataSet = new vis.DataSet(rawNodes);
      edgesDataSet = new vis.DataSet(rawEdges);

      const options = {{
        nodes: {{
          shape: 'dot',
          scaling: {{ min: 6, max: 48 }}
        }},
        edges: {{
          smooth: false, // smooth: false allows rendering thousands of edges at high FPS
          arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }}
        }},
        physics: {{
          solver: 'forceAtlas2Based',
          forceAtlas2Based: {{
            gravitationalConstant: -38,
            centralGravity: 0.005,
            springLength: 80,
            springConstant: 0.06,
            damping: 0.45,
            avoidOverlap: 0.3
          }},
          stabilization: {{
            iterations: 80,
            updateInterval: 20
          }}
        }},
        interaction: {{
          hover: true,
          tooltipDelay: 100,
          hideEdgesOnDrag: true
        }}
      }};

      network = new vis.Network(container, {{ nodes: nodesDataSet, edges: edgesDataSet }}, options);

      network.on("stabilizationIterationsDone", function () {{
        const loader = document.getElementById('loading-overlay');
        loader.style.opacity = '0';
        setTimeout(() => {{ loader.style.display = 'none'; }}, 400);
      }});

      // Click node
      network.on("click", function(params) {{
        if (params.nodes.length > 0) {{
          const selId = params.nodes[0];
          showInspector(selId);
          highlightEgo(selId);
        }} else {{
          hideInspector();
          resetHighlight();
        }}
      }});

      setupControls();
    }});

    function showInspector(nodeId) {{
      const node = rawNodes.find(n => n.id === nodeId);
      if (!node) return;

      const m = node.meta || {{}};
      const panel = document.getElementById('inspector');
      panel.style.display = 'flex';

      document.getElementById('insp-title').innerText = m.number || node.label || nodeId;
      const badge = document.getElementById('insp-badge');
      if (m.jurisdiction === 'local') {{
        badge.className = 'inspector-badge badge-loc';
        badge.innerText = 'Davao City Local Ordinance';
      }} else {{
        badge.className = 'inspector-badge badge-nat';
        badge.innerText = 'National Statute';
      }}

      document.getElementById('insp-degree').innerText = m.degree || '-';
      document.getElementById('insp-year').innerText = m.year || '-';
      document.getElementById('insp-domain').innerText = m.domain || '-';
      document.getElementById('insp-title-full').innerText = m.title || 'No official title registered.';

      // Connected nodes
      const conns = rawEdges.filter(e => e.from === nodeId || e.to === nodeId);
      document.getElementById('insp-conn-count').innerText = conns.length;
      const connDiv = document.getElementById('insp-connections');
      connDiv.innerHTML = conns.slice(0, 20).map(e => {{
        const otherId = e.from === nodeId ? e.to : e.from;
        const otherNode = rawNodes.find(n => n.id === otherId);
        const name = otherNode ? (otherNode.meta?.number || otherNode.label || otherId) : otherId;
        const arrow = e.from === nodeId ? '→' : '←';
        return `<div><span style="color:#00f2fe;font-weight:600;">${{e.relation}}</span> ${{arrow}} ${{name}}</div>`;
      }}).join('');
    }}

    function hideInspector() {{
      document.getElementById('inspector').style.display = 'none';
    }}

    function highlightEgo(selectedId) {{
      const ego = new Set([selectedId]);
      rawEdges.forEach(e => {{
        if (e.from === selectedId) ego.add(e.to);
        if (e.to === selectedId) ego.add(e.from);
      }});

      const updates = rawNodes.map(n => {{
        if (ego.has(n.id)) {{
          return {{ id: n.id, hidden: false, opacity: 1.0 }};
        }} else {{
          return {{ id: n.id, hidden: false, opacity: 0.08 }};
        }}
      }});
      nodesDataSet.update(updates);
    }}

    function resetHighlight() {{
      const updates = rawNodes.map(n => ({{ id: n.id, hidden: false, opacity: 1.0 }}));
      nodesDataSet.update(updates);
    }}

    function setupControls() {{
      document.getElementById('close-inspector').addEventListener('click', () => {{
        hideInspector();
        resetHighlight();
      }});

      // Search
      document.getElementById('search-input').addEventListener('input', (e) => {{
        const q = e.target.value.toLowerCase().trim();
        if (!q) {{
          resetHighlight();
          return;
        }}
        const match = rawNodes.find(n => 
          (n.label && n.label.toLowerCase().includes(q)) || 
          (n.id && n.id.toLowerCase().includes(q)) ||
          (n.meta && n.meta.number && n.meta.number.toLowerCase().includes(q))
        );
        if (match) {{
          network.focus(match.id, {{ scale: 1.4, animation: {{ duration: 700 }} }});
          network.selectNodes([match.id]);
          showInspector(match.id);
          highlightEgo(match.id);
        }}
      }});

      // Physics Toggle
      let physOn = true;
      document.getElementById('btn-physics').addEventListener('click', (e) => {{
        physOn = !physOn;
        network.setOptions({{ physics: {{ enabled: physOn }} }});
        e.target.innerText = physOn ? 'Physics On' : 'Physics Off';
        e.target.classList.toggle('active', physOn);
      }});

      // Recenter
      document.getElementById('btn-recenter').addEventListener('click', () => {{
        network.fit({{ animation: {{ duration: 800 }} }});
        resetHighlight();
        hideInspector();
      }});

      // Freeze positions
      document.getElementById('btn-freeze').addEventListener('click', () => {{
        network.storePositions();
        network.setOptions({{ physics: {{ enabled: false }} }});
        document.getElementById('btn-physics').innerText = 'Physics Off';
        document.getElementById('btn-physics').classList.remove('active');
      }});

      // Subsets toggle
      document.querySelectorAll('[data-filter]').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          document.querySelectorAll('[data-filter]').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
          const filter = e.target.getAttribute('data-filter');

          if (filter === 'all') {{
            resetHighlight();
          }} else {{
            const updates = rawNodes.map(n => {{
              const isMatch = n.group === filter;
              return {{
                id: n.id,
                opacity: isMatch ? 1.0 : 0.05
              }};
            }});
            nodesDataSet.update(updates);
          }}
        }});
      }});
    }}
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"SUCCESS: Full Corpus Web Graph written to '{OUTPUT_HTML}'!")
    print(f"File size: {os.path.getsize(OUTPUT_HTML) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()

