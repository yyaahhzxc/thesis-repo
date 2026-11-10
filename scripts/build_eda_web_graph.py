"""
build_eda_web_graph.py
======================
Builds the upgraded, high-precision Exploratory Data Analysis (EDA) web dashboard:
1. Expanded node selection: 3,500 active enactments (includes RA 1700, RA 7636, etc.)
2. Pixel-perfect cursor hit-testing: calculates distance in screen coordinates (sx, sy)
   with hover tooltip and inspection card, eliminating pointer displacement.
3. Enhanced "Trace Connection" tool:
   - Type selector: Republic Act (RA), Presidential Decree (PD), Batas Pambansa (BP),
     Commonwealth Act (CA), Executive Order (EO), Davao City Ordinance (ORD), or All.
   - Number input with automatic live suggestions/dropdown list showing matching laws.
4. Clean, pure organic web constellation by default (no text clutter, hover/click reveals).
"""

import json
import math
import os
import sys
import time
from collections import Counter
import networkx as nx

sys.path.insert(0, os.path.abspath("."))
from src.knowledge_graph.build_statutory_kg import build_alias_registry, extract_edges

OUTPUT_HTML = "output/visualizations/statutory_kg_full_web.html"

# High-contrast EDA Macro Domain Palette
DOMAIN_PALETTE = {
    "General Administration, Organization & Civil Service": "#38BDF8",  # Sky Blue
    "Public Finance, Taxation, Fiscal Policy & Budget": "#F59E0B",      # Amber
    "Police Power, Public Order, Safety & Penal Law": "#EF4444",        # Crimson
    "Social Services, Education, Labor & Human Development": "#10B981", # Emerald
    "Public Works, Transportation, Utilities & Infrastructure": "#8B5CF6",# Violet
    "Commerce, Trade, Industry, Agriculture & Economic Enterprise": "#06B6D4",# Cyan
    "Environmental Protection, Zoning, Land Use & Natural Resources": "#84CC16",# Lime
    "Executive Issuances & Policy Reorganization": "#EC4899",          # Pink
    "Inter-Agency Agreements & Institutional MOAs/MOUs": "#F97316",    # Orange
    "Substantive Regulatory, Health & Penal Ordinances": "#14B8A6"     # Teal
}

def get_era(year):
    if not year or year == "N/A":
        return "Unknown"
    try:
        y = int(year)
        if y < 1946:
            return "Pre-War & Commonwealth (<1946)"
        elif y < 1986:
            return "Third Republic & Martial Law (1946–1986)"
        elif y < 2016:
            return "Fifth Republic & Decentralization (1987–2015)"
        else:
            return "Modern Digital Era (2016–Present)"
    except:
        return "Unknown"

def main():
    print("[1/4] Ingesting enactment metadata and extracting citations/amendments...")
    meta, aliases = build_alias_registry()
    cites, amends, repeals = extract_edges(meta, aliases)

    # Degree counter
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

    # Select top 3,500 connected nodes (all connected local ordinances + top 2,500 national laws)
    local_candidates = [n for n in node_degree if meta.get(n, {}).get("jurisdiction") == "local"]
    local_candidates.sort(key=lambda x: node_degree[x], reverse=True)
    
    nat_candidates = [n for n in node_degree if meta.get(n, {}).get("jurisdiction") == "national"]
    nat_candidates.sort(key=lambda x: node_degree[x], reverse=True)

    selected_nodes = set(local_candidates[:1000] + nat_candidates[:2500])
    # Explicitly ensure RA 1700 and RA 7636 are in the visual web graph
    if "ra_1700_1957" in node_degree:
        selected_nodes.add("ra_1700_1957")
    if "ra_7636_1992" in node_degree:
        selected_nodes.add("ra_7636_1992")

    print(f"[2/4] Selected {len(selected_nodes):,} enactments for the visual graph.")

    G = nx.Graph()
    for n in selected_nodes:
        G.add_node(n)

    edges_typed = []
    for (u, v), w in cites.items():
        if u in selected_nodes and v in selected_nodes:
            G.add_edge(u, v, weight=min(3.0, 1.0 + w * 0.2))
            edges_typed.append({"u": u, "v": v, "t": "cites"})

    for (u, v) in amends:
        if u in selected_nodes and v in selected_nodes:
            G.add_edge(u, v, weight=2.5)
            edges_typed.append({"u": u, "v": v, "t": "amends"})

    for (u, v) in repeals:
        if u in selected_nodes and v in selected_nodes:
            G.add_edge(u, v, weight=2.5)
            edges_typed.append({"u": u, "v": v, "t": "repeals"})

    print(f"      Graph: {G.number_of_nodes():,} nodes, {len(edges_typed):,} edges.")

    print("[3/4] Precomputing force-directed organic spring layout in Python...")
    t0 = time.time()
    # scale to 4,200 space to allow 3,500 clusters to breathe naturally
    pos = nx.spring_layout(G, k=0.17, iterations=60, weight="weight", seed=42, scale=4200)
    print(f"      Spring layout completed in {time.time() - t0:.2f}s!")

    # Format nodes payload
    nodes_payload = []
    for nid in G.nodes():
        m = meta.get(nid, {})
        deg = node_degree[nid]
        is_local = m.get("jurisdiction") == "local"
        dom = m.get("domain", "General Administration, Organization & Civil Service")
        base_color = DOMAIN_PALETTE.get(dom, "#38BDF8")
        year = m.get("year", "N/A")
        era = get_era(year)

        x, y = pos[nid]

        if nid == "ra_7160_1991":
            radius = 38
            color = "#FFD700"
            label = "RA 7160 (Local Government Code)"
        elif deg >= 50:
            radius = min(26, max(12, int(8 + (deg ** 0.5) * 1.5)))
            color = "#FFB300" if not is_local else "#00F2FE"
            label = m.get("number", nid)
        elif deg >= 15:
            radius = min(15, max(8, int(5 + (deg ** 0.5) * 1.2)))
            color = base_color if not is_local else "#00F2FE"
            label = m.get("number", nid)
        elif is_local:
            radius = min(10, max(4, int(3 + (deg ** 0.5) * 1.0)))
            color = "#00F2FE"
            label = m.get("number", nid)
        else:
            radius = min(8, max(3, int(2.2 + (deg ** 0.5) * 0.7)))
            color = base_color
            label = m.get("number", nid)

        if label and len(label) > 24:
            label = label[:22] + ".."

        # Instrument classification for dropdown searching
        num_str = m.get("number", nid)
        inst_type = "OTHER"
        if is_local:
            inst_type = "ORD"
        elif "republic act" in num_str.lower() or "r.a." in num_str.lower() or "ra_" in nid:
            inst_type = "RA"
        elif "presidential decree" in num_str.lower() or "p.d." in num_str.lower() or "pd_" in nid:
            inst_type = "PD"
        elif "batas pambansa" in num_str.lower() or "b.p." in num_str.lower() or "bp_" in nid:
            inst_type = "BP"
        elif "executive order" in num_str.lower() or "e.o." in num_str.lower() or "eo_" in nid:
            inst_type = "EO"
        elif "commonwealth act" in num_str.lower() or "c.a." in num_str.lower() or "ca_" in nid:
            inst_type = "CA"
        elif "act no" in num_str.lower() or "act_" in nid:
            inst_type = "ACT"

        nodes_payload.append({
            "id": nid,
            "x": round(float(x), 1),
            "y": round(float(y), 1),
            "r": radius,
            "c": color,
            "label": label,
            "deg": deg,
            "jur": m.get("jurisdiction", "national"),
            "type": inst_type,
            "num": num_str,
            "year": year,
            "era": era,
            "dom": dom,
            "title": (m.get("title") or "")[:200]
        })

    print("[4/4] Writing EDA Constellation Web Dashboard HTML...")
    nodes_json = json.dumps(nodes_payload)
    edges_json = json.dumps(edges_typed)

    html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Statutory Knowledge Graph — Exploratory Data Analysis (EDA)</title>
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
      background: #05070b;
      color: #e2e8f0;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: rgba(9, 13, 22, 0.92);
      backdrop-filter: blur(14px);
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
      font-size: 15px;
      font-weight: 600;
      color: #f8fafc;
      letter-spacing: -0.3px;
    }}
    .stats-bar {{
      display: flex;
      align-items: center;
      gap: 12px;
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
      width: 100%;
      height: 100%;
    }}
    #graph-canvas {{
      display: block;
      width: 100%;
      height: 100%;
      cursor: grab;
      background: radial-gradient(circle at center, #0a0f1d 0%, #05070b 100%);
    }}
    #graph-canvas:active {{
      cursor: grabbing;
    }}
    /* EDA Filter Panel */
    .eda-panel {{
      position: absolute;
      top: 16px;
      left: 16px;
      width: 350px;
      max-height: calc(100% - 32px);
      background: rgba(11, 16, 28, 0.94);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 14px;
      overflow-y: auto;
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
    .filter-section {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .filter-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #64748b;
      font-weight: 700;
      display: flex;
      justify-content: space-between;
    }}
    .filter-dropdown {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 7px 10px;
      color: #f1f5f9;
      font-size: 12px;
      outline: none;
      cursor: pointer;
    }}
    .filter-dropdown option {{
      background: #0f172a;
      color: #fff;
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
    /* Path Finder Law Selectors */
    .law-selector-row {{
      display: flex;
      gap: 6px;
    }}
    .type-select {{
      width: 80px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 6px 4px;
      color: #00f2fe;
      font-size: 11px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }}
    .type-select option {{
      background: #0f172a;
      color: #fff;
    }}
    .num-input-wrapper {{
      position: relative;
      flex: 1;
    }}
    .num-input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 6px 8px;
      color: #f1f5f9;
      font-size: 11px;
      outline: none;
    }}
    .suggestions-list {{
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: #0f172a;
      border: 1px solid #00f2fe;
      border-radius: 6px;
      max-height: 140px;
      overflow-y: auto;
      z-index: 50;
      display: none;
      box-shadow: 0 10px 20px rgba(0,0,0,0.8);
    }}
    .suggestion-item {{
      padding: 6px 8px;
      font-size: 11px;
      cursor: pointer;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .suggestion-item:hover {{
      background: #1e293b;
      color: #00f2fe;
    }}
    /* Slider */
    .slider-container {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .slider-container input[type=range] {{
      flex: 1;
      accent-color: #00f2fe;
      cursor: pointer;
    }}
    .slider-val {{
      font-family: 'Fira Code', monospace;
      font-size: 12px;
      color: #00f2fe;
      min-width: 34px;
      text-align: right;
    }}
    /* Inspector Card */
    .inspector-card {{
      position: absolute;
      top: 16px;
      right: 16px;
      width: 360px;
      max-height: calc(100% - 32px);
      background: rgba(11, 16, 28, 0.94);
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
    /* Floating Tooltip */
    #hover-tooltip {{
      position: absolute;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #00f2fe;
      color: #f8fafc;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      pointer-events: none;
      z-index: 100;
      display: none;
      box-shadow: 0 8px 24px rgba(0,0,0,0.8);
      white-space: nowrap;
      transform: translate(-50%, -140%);
    }}
    /* Nav Zoom Controls */
    .zoom-controls {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      z-index: 10;
    }}
    .zoom-btn {{
      width: 36px;
      height: 36px;
      background: rgba(11, 16, 28, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      color: #f8fafc;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      backdrop-filter: blur(12px);
    }}
    .zoom-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      border-color: #00f2fe;
    }}
    /* Legend */
    .legend {{
      position: absolute;
      bottom: 24px;
      left: 16px;
      background: rgba(11, 16, 28, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 8px 14px;
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
      width: 9px;
      height: 9px;
      border-radius: 50%;
    }}
  </style>
</head>
<body>

  <div id="hover-tooltip"></div>

  <header>
    <div class="brand">
      <span class="badge">EDA Web Explorer</span>
      <h1>Philippine Statutory Knowledge Graph — Topological EDA</h1>
    </div>
    <div class="stats-bar">
      <div class="stat-pill">
        <span>Active Vertices:</span>
        <span class="stat-val" id="stat-visible-nodes">{len(nodes_payload):,}</span>
      </div>
      <div class="stat-pill">
        <span>Relational Arcs:</span>
        <span class="stat-val" id="stat-visible-edges">{len(edges_typed):,}</span>
      </div>
      <div class="stat-pill">
        <span>Davao Integration:</span>
        <span class="stat-val">78.7% GCC</span>
      </div>
    </div>
  </header>

  <div class="main-container">
    <!-- EDA Filter Panel -->
    <div class="eda-panel">
      <!-- 2-Law Path & Distance Finder -->
      <div class="filter-section" style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 10px;">
        <div class="filter-label" style="color: #00F2FE;">
          <span>Trace Connection Between 2 Laws</span>
          <span id="path-distance-badge" style="font-family:'Fira Code'; font-size:10px; color:#FFD700; background:rgba(255,215,0,0.1); padding:2px 6px; border-radius:4px; display:none;">Distance: 2 hops</span>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
          <!-- Law A Selector -->
          <div>
            <div style="font-size:10px; color:#94a3b8; margin-bottom:2px;">LAW A:</div>
            <div class="law-selector-row">
              <select id="type-select-a" class="type-select">
                <option value="ALL">All</option>
                <option value="RA" selected>RA</option>
                <option value="ORD">Ordinance</option>
                <option value="PD">PD</option>
                <option value="BP">BP</option>
                <option value="EO">EO</option>
                <option value="CA">CA</option>
                <option value="ACT">Act</option>
              </select>
              <div class="num-input-wrapper">
                <input type="text" id="path-input-a" class="num-input" placeholder="Type number (e.g. 1700, 0270)..." autocomplete="off">
                <div id="suggest-a" class="suggestions-list"></div>
              </div>
            </div>
          </div>

          <!-- Law B Selector -->
          <div>
            <div style="font-size:10px; color:#94a3b8; margin-bottom:2px;">LAW B:</div>
            <div class="law-selector-row">
              <select id="type-select-b" class="type-select">
                <option value="ALL">All</option>
                <option value="RA" selected>RA</option>
                <option value="ORD">Ordinance</option>
                <option value="PD">PD</option>
                <option value="BP">BP</option>
                <option value="EO">EO</option>
                <option value="CA">CA</option>
                <option value="ACT">Act</option>
              </select>
              <div class="num-input-wrapper">
                <input type="text" id="path-input-b" class="num-input" placeholder="Type number (e.g. 7636, 7160)..." autocomplete="off">
                <div id="suggest-b" class="suggestions-list"></div>
              </div>
            </div>
          </div>

          <div class="btn-row" style="margin-top: 4px;">
            <button class="toggle-btn" id="btn-trace-path" style="background:#00F2FE; color:#07090e; font-weight:700; flex:1;">Find Path</button>
            <button class="toggle-btn" id="btn-clear-path" style="flex:1;">Clear Path</button>
          </div>
          <div id="path-status" style="font-size:11px; color:#94a3b8; line-height:1.4; margin-top:2px; display:none;"></div>
        </div>
      </div>

      <div class="search-box">
        <input type="text" id="search-input" placeholder="Search individual law, keyword...">
      </div>

      <!-- Jurisdiction Filter -->
      <div class="filter-section">
        <div class="filter-label">1. Jurisdiction Partition</div>
        <div class="btn-row">
          <button class="toggle-btn active" data-jur="all">All</button>
          <button class="toggle-btn" data-jur="local">Davao Ordinances</button>
          <button class="toggle-btn" data-jur="national">National Statutes</button>
        </div>
      </div>

      <!-- Macro Domain Filter -->
      <div class="filter-section">
        <div class="filter-label">2. Macro Legal Domain</div>
        <select id="domain-select" class="filter-dropdown">
          <option value="all">All Domains (Multi-Disciplinary)</option>
          <option value="General Administration, Organization & Civil Service">General Administration & LGU</option>
          <option value="Public Finance, Taxation, Fiscal Policy & Budget">Public Finance & Taxation</option>
          <option value="Police Power, Public Order, Safety & Penal Law">Police Power, Safety & Penal</option>
          <option value="Social Services, Education, Labor & Human Development">Social Services & Labor</option>
          <option value="Public Works, Transportation, Utilities & Infrastructure">Public Works & Transport</option>
          <option value="Commerce, Trade, Industry, Agriculture & Economic Enterprise">Commerce, Trade & Agriculture</option>
          <option value="Environmental Protection, Zoning, Land Use & Natural Resources">Environmental & Natural Resources</option>
          <option value="Executive Issuances & Policy Reorganization">Executive Policy & Directives</option>
        </select>
      </div>

      <!-- Temporal Era Filter -->
      <div class="filter-section">
        <div class="filter-label">3. Legislative Era (Evolution)</div>
        <select id="era-select" class="filter-dropdown">
          <option value="all">All Eras (1900–Present)</option>
          <option value="Pre-War & Commonwealth (<1946)">Pre-War & Commonwealth (<1946)</option>
          <option value="Third Republic & Martial Law (1946–1986)">Third Republic & Martial Law (1946–1986)</option>
          <option value="Fifth Republic & Decentralization (1987–2015)">Fifth Republic & Decentralization (1987–2015)</option>
          <option value="Modern Digital Era (2016–Present)">Modern Digital Era (2016–Present)</option>
        </select>
      </div>

      <!-- Edge Type Filter -->
      <div class="filter-section">
        <div class="filter-label">4. Relational Edge Vocabulary</div>
        <div class="btn-row">
          <button class="toggle-btn active" data-edge="all">All Relations</button>
          <button class="toggle-btn" data-edge="cites">Citations</button>
          <button class="toggle-btn" data-edge="amends">Amendments</button>
          <button class="toggle-btn" data-edge="repeals">Repeals</button>
        </div>
      </div>

      <!-- Min Connectivity Degree Slider -->
      <div class="filter-section">
        <div class="filter-label">
          <span>5. Min Connectivity (Degree)</span>
          <span class="slider-val" id="degree-val">1</span>
        </div>
        <div class="slider-container">
          <input type="range" id="degree-slider" min="1" max="40" value="1" step="1">
        </div>
      </div>

      <!-- View Reset Controls -->
      <div class="filter-section" style="margin-top: 4px;">
        <div class="btn-row">
          <button class="toggle-btn" id="btn-recenter" style="flex:1;">Recenter Graph</button>
          <button class="toggle-btn" id="btn-toggle-labels" style="flex:1;">Toggle Hub Labels</button>
        </div>
      </div>
    </div>

    <!-- Canvas -->
    <canvas id="graph-canvas"></canvas>

    <!-- Zoom Controls -->
    <div class="zoom-controls">
      <button class="zoom-btn" id="btn-zoom-in">+</button>
      <button class="zoom-btn" id="btn-zoom-out">&minus;</button>
      <button class="zoom-btn" id="btn-reset" title="Reset View">&#x2302;</button>
    </div>

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
        <div class="metric-card" style="grid-column: span 2;">
          <div class="metric-label">Historical Era</div>
          <div class="metric-val" id="insp-era" style="color: #38bdf8;">Fifth Republic</div>
        </div>
      </div>

      <div>
        <div class="filter-label" style="margin-bottom: 6px;">Statutory Long Title</div>
        <div class="text-block" id="insp-title-full"></div>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend">
      <div class="legend-item">
        <span class="legend-dot" style="background: #FFD700;"></span>
        <span>National Super-Hub (RA 7160 / 9184)</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #00F2FE;"></span>
        <span>Davao City Local Ordinance</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #F59E0B;"></span>
        <span>Public Finance & Tax</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #EF4444;"></span>
        <span>Penal & Police Power</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #84CC16;"></span>
        <span>Environment & Zoning</span>
      </div>
    </div>
  </div>

  <script>
    const NODES = {nodes_json};
    const EDGES = {edges_json};

    const nodeMap = new Map();
    NODES.forEach(n => nodeMap.set(n.id, n));

    // Build Adjacency List for Shortest Path BFS
    const adj = new Map();
    NODES.forEach(n => adj.set(n.id, []));
    EDGES.forEach(e => {{
      if (adj.has(e.u) && adj.has(e.v)) {{
        adj.get(e.u).push({{ target: e.v, type: e.t }});
        adj.get(e.v).push({{ target: e.u, type: e.t }});
      }}
    }});

    let activePathNodes = null;
    let activePathEdges = null;
    let pathStartNode = null;
    let pathEndNode = null;

    const canvas = document.getElementById('graph-canvas');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('hover-tooltip');

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {{
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      render();
    }});

    // Camera transform (Pan & Zoom)
    let zoom = 0.25;
    let panX = width / 2;
    let panY = height / 2;

    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;

    let hoveredNode = null;
    let selectedNode = null;
    let showHubLabels = false;

    // Active EDA Filters
    let filterJur = 'all';
    let filterDomain = 'all';
    let filterEra = 'all';
    let filterEdge = 'all';
    let filterMinDegree = 1;

    function toScreenX(x) {{ return x * zoom + panX; }}
    function toScreenY(y) {{ return y * zoom + panY; }}
    function toWorldX(sx) {{ return (sx - panX) / zoom; }}
    function toWorldY(sy) {{ return (sy - panY) / zoom; }}

    function isNodeVisible(n) {{
      if (filterJur !== 'all' && n.jur !== filterJur) return false;
      if (filterDomain !== 'all' && n.dom !== filterDomain) return false;
      if (filterEra !== 'all' && n.era !== filterEra) return false;
      if (n.deg < filterMinDegree) return false;
      return true;
    }}

    function findShortestPath(startId, endId) {{
      if (startId === endId) return {{ distance: 0, path: [startId] }};
      const queue = [[startId]];
      const visited = new Set([startId]);

      while (queue.length > 0) {{
        const currentPath = queue.shift();
        const current = currentPath[currentPath.length - 1];

        const neighbors = adj.get(current) || [];
        for (let i = 0; i < neighbors.length; i++) {{
          const neighbor = neighbors[i].target;
          if (neighbor === endId) {{
            currentPath.push(neighbor);
            return {{ distance: currentPath.length - 1, path: currentPath }};
          }}
          if (!visited.has(neighbor)) {{
            visited.add(neighbor);
            queue.push([...currentPath, neighbor]);
          }}
        }}
      }}
      return null;
    }}

    function render() {{
      ctx.clearRect(0, 0, width, height);

      let visibleNodesCount = 0;
      let visibleEdgesCount = 0;

      // 1. Draw Edges
      for (let i = 0; i < EDGES.length; i++) {{
        const edge = EDGES[i];
        if (filterEdge !== 'all' && edge.t !== filterEdge) continue;

        const u = nodeMap.get(edge.u);
        const v = nodeMap.get(edge.v);
        if (!u || !v) continue;

        if (!isNodeVisible(u) || !isNodeVisible(v)) continue;

        visibleEdgesCount++;

        const isPathEdge = activePathEdges && (activePathEdges.has(`${{u.id}}|${{v.id}}`) || activePathEdges.has(`${{v.id}}|${{u.id}}`));
        const isHighlighted = (selectedNode && (u.id === selectedNode.id || v.id === selectedNode.id)) ||
                              (hoveredNode && (u.id === hoveredNode.id || v.id === hoveredNode.id));

        if (isPathEdge) {{
          ctx.strokeStyle = '#FFD700';
          ctx.lineWidth = 3.5;
        }} else if (activePathNodes) {{
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        }} else if (isHighlighted) {{
          ctx.strokeStyle = '#00F2FE';
          ctx.lineWidth = 2.2;
        }} else if (selectedNode) {{
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        }} else {{
          if (edge.t === 'amends') {{
            ctx.strokeStyle = 'rgba(255, 165, 0, 0.45)';
            ctx.lineWidth = 1.0;
          }} else if (edge.t === 'repeals') {{
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)';
            ctx.lineWidth = 1.2;
          }} else {{
            ctx.strokeStyle = 'rgba(100, 150, 255, 0.18)';
            ctx.lineWidth = 0.6;
          }}
        }}

        ctx.beginPath();
        ctx.moveTo(toScreenX(u.x), toScreenY(u.y));
        ctx.lineTo(toScreenX(v.x), toScreenY(v.y));
        ctx.stroke();
      }}

      // 2. Draw Nodes
      for (let i = 0; i < NODES.length; i++) {{
        const n = NODES[i];
        if (!isNodeVisible(n)) continue;

        visibleNodesCount++;

        const sx = toScreenX(n.x);
        const sy = toScreenY(n.y);

        if (sx < -100 || sx > width + 100 || sy < -100 || sy > height + 100) continue;

        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isSelected = selectedNode && selectedNode.id === n.id;
        const isPathNode = activePathNodes && activePathNodes.has(n.id);
        const isPathEndpoint = pathStartNode && (n.id === pathStartNode.id || (pathEndNode && n.id === pathEndNode.id));
        const sr = Math.max(2.2, n.r * zoom * (isPathEndpoint ? 1.5 : (isPathNode ? 1.25 : 1.0)));

        ctx.beginPath();
        ctx.arc(sx, sy, sr, 0, Math.PI * 2);

        if (isPathEndpoint) {{
          ctx.fillStyle = '#FFD700';
          ctx.shadowColor = '#FFD700';
          ctx.shadowBlur = 24;
        }} else if (isPathNode) {{
          ctx.fillStyle = '#00F2FE';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        }} else if (activePathNodes) {{
          ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
          ctx.shadowBlur = 0;
        }} else if (isHovered || isSelected) {{
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        }} else {{
          ctx.fillStyle = n.c;
          ctx.shadowBlur = 0;
        }}
        ctx.fill();

        if (n.id === 'ra_7160_1991') {{
          ctx.strokeStyle = '#FFD700';
          ctx.lineWidth = 2.5;
          ctx.stroke();
        }}

        // 3. Draw Labels ONLY on Hover, Selection, Active Path, or if toggled
        const shouldDrawLabel = isHovered || isSelected || (activePathNodes && activePathNodes.has(n.id)) || (showHubLabels && (n.id === 'ra_7160_1991' || n.deg >= 60));
        if (shouldDrawLabel && n.label) {{
          const fontSize = Math.max(10, Math.min(14, 11 * zoom));
          ctx.font = `600 ${{fontSize}}px Inter, sans-serif`;
          ctx.fillStyle = isHovered || isSelected ? '#00F2FE' : (isPathEndpoint ? '#FFD700' : '#F1F5F9');
          ctx.shadowColor = '#000000';
          ctx.shadowBlur = 4;
          ctx.fillText(n.label, sx + sr + 5, sy + fontSize / 3);
          ctx.shadowBlur = 0;
        }}
      }}

      document.getElementById('stat-visible-nodes').innerText = visibleNodesCount.toLocaleString();
      document.getElementById('stat-visible-edges').innerText = visibleEdgesCount.toLocaleString();
    }}

    // Accurate Screen-Space Hit-Testing (Fixes Mouse Highlight Displacement!)
    function getNodeAtScreenPos(mouseX, mouseY) {{
      for (let i = NODES.length - 1; i >= 0; i--) {{
        const n = NODES[i];
        if (!isNodeVisible(n)) continue;
        const sx = toScreenX(n.x);
        const sy = toScreenY(n.y);
        const dx = sx - mouseX;
        const dy = sy - mouseY;
        const hitRadius = Math.max(8, n.r * zoom + 5);
        if (dx * dx + dy * dy <= hitRadius * hitRadius) {{
          return n;
        }}
      }}
      return null;
    }}

    canvas.addEventListener('mousedown', (e) => {{
      isDragging = true;
      dragStartX = e.clientX - panX;
      dragStartY = e.clientY - panY;
      tooltip.style.display = 'none';
    }});

    window.addEventListener('mousemove', (e) => {{
      if (isDragging) {{
        panX = e.clientX - dragStartX;
        panY = e.clientY - dragStartY;
        tooltip.style.display = 'none';
        render();
        return;
      }}

      const found = getNodeAtScreenPos(e.clientX, e.clientY);

      if (found !== hoveredNode) {{
        hoveredNode = found;
        render();
      }}

      if (hoveredNode) {{
        const sx = toScreenX(hoveredNode.x);
        const sy = toScreenY(hoveredNode.y);
        tooltip.style.display = 'block';
        tooltip.style.left = `${{sx}}px`;
        tooltip.style.top = `${{sy}}px`;
        tooltip.innerHTML = `<span style="color:#00F2FE;">${{hoveredNode.num || hoveredNode.id}}</span> <span style="color:#94a3b8; font-size:10px;">(Degree: ${{hoveredNode.deg}})</span>`;
      }} else {{
        tooltip.style.display = 'none';
      }}
    }});

    window.addEventListener('mouseup', () => {{
      isDragging = false;
    }});

    canvas.addEventListener('wheel', (e) => {{
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const mouseWorldX = toWorldX(e.clientX);
      const mouseWorldY = toWorldY(e.clientY);

      zoom = Math.max(0.05, Math.min(4.5, zoom * zoomFactor));

      panX = e.clientX - mouseWorldX * zoom;
      panY = e.clientY - mouseWorldY * zoom;

      render();
    }}, {{ passive: false }});

    canvas.addEventListener('click', (e) => {{
      const found = getNodeAtScreenPos(e.clientX, e.clientY);
      if (found) {{
        selectedNode = found;
        showInspector(selectedNode);
        render();
      }} else {{
        selectedNode = null;
        hideInspector();
        render();
      }}
    }});

    function showInspector(n) {{
      const card = document.getElementById('inspector');
      card.style.display = 'flex';

      document.getElementById('insp-title').innerText = n.num || n.id;
      const badge = document.getElementById('insp-badge');
      if (n.jur === 'local') {{
        badge.className = 'inspector-badge badge-loc';
        badge.innerText = 'Davao City Local Ordinance';
      }} else {{
        badge.className = 'inspector-badge badge-nat';
        badge.innerText = `${{n.type || 'National'}} Statute`;
      }}

      document.getElementById('insp-degree').innerText = n.deg;
      document.getElementById('insp-year').innerText = n.year;
      document.getElementById('insp-domain').innerText = n.dom;
      document.getElementById('insp-era').innerText = n.era;
      document.getElementById('insp-title-full').innerText = n.title || 'Official positive law enactment.';
    }}

    function hideInspector() {{
      document.getElementById('inspector').style.display = 'none';
      selectedNode = null;
    }}

    document.getElementById('close-inspector').addEventListener('click', hideInspector);

    // Zoom Buttons
    document.getElementById('btn-zoom-in').addEventListener('click', () => {{
      zoom = Math.min(4.5, zoom * 1.3);
      render();
    }});
    document.getElementById('btn-zoom-out').addEventListener('click', () => {{
      zoom = Math.max(0.05, zoom * 0.7);
      render();
    }});
    document.getElementById('btn-reset').addEventListener('click', () => {{
      zoom = 0.25;
      panX = width / 2;
      panY = height / 2;
      render();
    }});
    document.getElementById('btn-recenter').addEventListener('click', () => {{
      zoom = 0.25;
      panX = width / 2;
      panY = height / 2;
      render();
    }});

    document.getElementById('btn-toggle-labels').addEventListener('click', (e) => {{
      showHubLabels = !showHubLabels;
      e.target.classList.toggle('active', showHubLabels);
      render();
    }});

    document.querySelectorAll('[data-jur]').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        document.querySelectorAll('[data-jur]').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        filterJur = e.target.getAttribute('data-jur');
        render();
      }});
    }});

    document.getElementById('domain-select').addEventListener('change', (e) => {{
      filterDomain = e.target.value;
      render();
    }});

    document.getElementById('era-select').addEventListener('change', (e) => {{
      filterEra = e.target.value;
      render();
    }});

    document.querySelectorAll('[data-edge]').forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        document.querySelectorAll('[data-edge]').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        filterEdge = e.target.getAttribute('data-edge');
        render();
      }});
    }});

    const slider = document.getElementById('degree-slider');
    const sliderVal = document.getElementById('degree-val');
    slider.addEventListener('input', (e) => {{
      filterMinDegree = parseInt(e.target.value);
      sliderVal.innerText = filterMinDegree;
      render();
    }});

    // Helper: Find law nodes by type and number query
    function searchLaws(type, query) {{
      query = (query || '').toLowerCase().trim();
      return NODES.filter(n => {{
        if (type !== 'ALL' && n.type !== type) return false;
        if (!query) return true;
        return (n.num && n.num.toLowerCase().includes(query)) ||
               (n.id && n.id.toLowerCase().includes(query));
      }});
    }}

    function setupSuggestions(inputId, typeSelectId, listId) {{
      const input = document.getElementById(inputId);
      const typeSelect = document.getElementById(typeSelectId);
      const list = document.getElementById(listId);

      function update() {{
        const q = input.value.trim();
        const type = typeSelect.value;
        const matches = searchLaws(type, q).slice(0, 8);

        if (matches.length === 0 || !q) {{
          list.style.display = 'none';
          return;
        }}

        list.innerHTML = matches.map(m => `
          <div class="suggestion-item" data-id="${{m.id}}">
            <span style="color:#00F2FE; font-weight:600;">${{m.num || m.id}}</span>
            <span style="color:#64748b; font-size:10px; margin-left:4px;">(${{m.year}})</span>
          </div>
        `).join('');
        list.style.display = 'block';

        list.querySelectorAll('.suggestion-item').forEach(item => {{
          item.addEventListener('click', () => {{
            const nid = item.getAttribute('data-id');
            const found = nodeMap.get(nid);
            if (found) {{
              input.value = found.num || found.id;
              input.dataset.selectedId = found.id;
            }}
            list.style.display = 'none';
          }});
        }});
      }}

      input.addEventListener('input', update);
      input.addEventListener('focus', update);
      typeSelect.addEventListener('change', update);

      document.addEventListener('click', (e) => {{
        if (!input.contains(e.target) && !list.contains(e.target)) {{
          list.style.display = 'none';
        }}
      }});
    }}

    setupSuggestions('path-input-a', 'type-select-a', 'suggest-a');
    setupSuggestions('path-input-b', 'type-select-b', 'suggest-b');

    // 2-Law Pathfinding Handler
    document.getElementById('btn-trace-path').addEventListener('click', () => {{
      const inputA = document.getElementById('path-input-a');
      const inputB = document.getElementById('path-input-b');
      const typeA = document.getElementById('type-select-a').value;
      const typeB = document.getElementById('type-select-b').value;
      const statusDiv = document.getElementById('path-status');
      const badge = document.getElementById('path-distance-badge');

      statusDiv.style.display = 'block';

      const qA = inputA.value.trim();
      const qB = inputB.value.trim();

      if (!qA || !qB) {{
        statusDiv.innerHTML = '<span style="color:#EF4444;">Please specify both Law A and Law B.</span>';
        return;
      }}

      // Find node A
      let nodeA = inputA.dataset.selectedId ? nodeMap.get(inputA.dataset.selectedId) : null;
      if (!nodeA) {{
        const matchesA = searchLaws(typeA, qA);
        nodeA = matchesA[0];
      }}

      // Find node B
      let nodeB = inputB.dataset.selectedId ? nodeMap.get(inputB.dataset.selectedId) : null;
      if (!nodeB) {{
        const matchesB = searchLaws(typeB, qB);
        nodeB = matchesB[0];
      }}

      if (!nodeA) {{
        statusDiv.innerHTML = `<span style="color:#EF4444;">Law A ("${{qA}}") not found in active graph.</span>`;
        return;
      }}
      if (!nodeB) {{
        statusDiv.innerHTML = `<span style="color:#EF4444;">Law B ("${{qB}}") not found in active graph.</span>`;
        return;
      }}

      const res = findShortestPath(nodeA.id, nodeB.id);
      if (!res) {{
        statusDiv.innerHTML = `<span style="color:#F59E0B;">No direct or intermediate path connects <b>${{nodeA.num}}</b> and <b>${{nodeB.num}}</b>.</span>`;
        badge.style.display = 'none';
        activePathNodes = null;
        activePathEdges = null;
        render();
        return;
      }}

      pathStartNode = nodeA;
      pathEndNode = nodeB;
      activePathNodes = new Set(res.path);
      activePathEdges = new Set();
      for (let i = 0; i < res.path.length - 1; i++) {{
        activePathEdges.add(`${{res.path[i]}}|${{res.path[i+1]}}`);
      }}

      badge.style.display = 'inline-block';
      badge.innerText = `Distance: ${{res.distance}} hop${{res.distance === 1 ? '' : 's'}}`;

      const pathSteps = res.path.map((nid, idx) => {{
        const n = nodeMap.get(nid);
        const name = n.num || nid;
        return `<span style="color:${{idx === 0 || idx === res.path.length-1 ? '#FFD700' : '#00F2FE'}}; font-weight:600;">${{name}}</span>`;
      }}).join(' &rarr; ');

      statusDiv.innerHTML = `<div style="margin-bottom:4px; color:#F1F5F9;">Connected via <b>${{res.distance}} hop${{res.distance === 1 ? '' : 's'}}</b>:</div><div>${{pathSteps}}</div>`;

      const midX = (nodeA.x + nodeB.x) / 2;
      const midY = (nodeA.y + nodeB.y) / 2;
      const distSpan = Math.sqrt((nodeA.x - nodeB.x)**2 + (nodeA.y - nodeB.y)**2);
      zoom = Math.max(0.18, Math.min(1.4, (width * 0.5) / (distSpan + 300)));
      panX = width / 2 - midX * zoom;
      panY = height / 2 - midY * zoom;

      render();
    }});

    document.getElementById('btn-clear-path').addEventListener('click', () => {{
      activePathNodes = null;
      activePathEdges = null;
      pathStartNode = null;
      pathEndNode = null;
      document.getElementById('path-status').style.display = 'none';
      document.getElementById('path-distance-badge').style.display = 'none';
      document.getElementById('path-input-a').value = '';
      document.getElementById('path-input-b').value = '';
      delete document.getElementById('path-input-a').dataset.selectedId;
      delete document.getElementById('path-input-b').dataset.selectedId;
      render();
    }});

    // General search bar
    document.getElementById('search-input').addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase().trim();
      if (!q) {{
        selectedNode = null;
        render();
        return;
      }}
      const found = NODES.find(n => 
        (n.num && n.num.toLowerCase().includes(q)) ||
        (n.id && n.id.toLowerCase().includes(q)) ||
        (n.title && n.title.toLowerCase().includes(q))
      );
      if (found) {{
        selectedNode = found;
        zoom = 1.1;
        panX = width / 2 - found.x * zoom;
        panY = height / 2 - found.y * zoom;
        showInspector(found);
        render();
      }}
    }});

    render();
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"SUCCESS: Enhanced EDA Web Dashboard with precise hit-testing written to '{OUTPUT_HTML}'!")

if __name__ == "__main__":
    main()
