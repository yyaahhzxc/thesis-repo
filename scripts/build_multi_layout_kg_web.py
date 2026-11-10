"""
build_multi_layout_kg_web.py
============================
Precomputes 5 distinct topological and analytical layout perspectives
for all 27,248 enactments in the Philippine Statutory Knowledge Graph:

1. Repulsion Organic Web (Force-Directed Spring Physics - Image 2 galaxy style)
2. National Domain Topic Constellations (10 Domain Galaxies based on Dual-Corpus Topic Models)
3. Vertical Preemption Hierarchy (Lex Superior Top-to-Bottom Architecture)
4. Concentric Planetary Orbits (RA 7160 Local Government Code Ego-Centric Core)
5. Polar / Radial Wedges (Multi-polar Domain Centrality Fan)

Embeds all 5 coordinate sets directly into statutory_kg_full_web.html
with a smooth 60 FPS interpolation animation engine and an intuitive UI dropdown.
"""

import json
import math
import os
import random
import sys
import time
from collections import Counter, defaultdict
import networkx as nx

random.seed(42)

NODES_FILE = 'data/knowledge_graph/statutory_kg_nodes.jsonl'
EDGES_FILE = 'data/knowledge_graph/statutory_kg_edges.jsonl'
OUTPUT_HTML = 'output/visualizations/statutory_kg_full_web.html'

# 10 Canonical Macro-Domains from Dual-Corpus Topic Modeling
MACRO_DOMAINS = [
    "General Administration, Organization & Civil Service",
    "Public Finance, Taxation, Fiscal Policy & Budget",
    "Police Power, Public Order, Safety & Penal Law",
    "Social Services, Education, Labor & Human Development",
    "Public Works, Transportation, Utilities & Infrastructure",
    "Commerce, Trade, Industry, Agriculture & Economic Enterprise",
    "Environmental Protection, Zoning, Land Use & Natural Resources",
    "Executive Issuances & Policy Reorganization",
    "Inter-Agency Agreements & Institutional MOAs/MOUs",
    "Substantive Regulatory, Health & Penal Ordinances"
]

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

# Domain mapping for slight naming variations
DOMAIN_MAP = {
    "General Administration, Organization & Civil Service": "General Administration, Organization & Civil Service",
    "Local Government & Territorial Boundaries": "General Administration, Organization & Civil Service",
    "Statutory Codes & General Legal Amendments": "General Administration, Organization & Civil Service",
    "Public Finance, Taxation, Fiscal Policy & Budget": "Public Finance, Taxation, Fiscal Policy & Budget",
    "Public Finance & General Appropriations": "Public Finance, Taxation, Fiscal Policy & Budget",
    "Taxation, Tariffs & Revenue Administration": "Public Finance, Taxation, Fiscal Policy & Budget",
    "Police Power, Public Order, Safety & Penal Law": "Police Power, Public Order, Safety & Penal Law",
    "Social Services, Education, Labor & Human Development": "Social Services, Education, Labor & Human Development",
    "Education & Academic Institutions": "Social Services, Education, Labor & Human Development",
    "Public Health, Hospitals & Medical Services": "Social Services, Education, Labor & Human Development",
    "Public Works, Transportation, Utilities & Infrastructure": "Public Works, Transportation, Utilities & Infrastructure",
    "Public Utilities & Telecommunications Franchises": "Public Works, Transportation, Utilities & Infrastructure",
    "Temporary Road Closures & Traffic Management": "Public Works, Transportation, Utilities & Infrastructure",
    "Commerce, Trade, Industry, Agriculture & Economic Enterprise": "Commerce, Trade, Industry, Agriculture & Economic Enterprise",
    "Environmental Protection, Zoning, Land Use & Natural Resources": "Environmental Protection, Zoning, Land Use & Natural Resources",
    "Zoning Reclassifications & Subdivision Development": "Environmental Protection, Zoning, Land Use & Natural Resources",
    "Executive Issuances & Policy Reorganization": "Executive Issuances & Policy Reorganization",
    "Inter-Agency Agreements & Institutional MOAs/MOUs": "Inter-Agency Agreements & Institutional MOAs/MOUs",
    "Deeds of Donation & Property Usufruct": "Inter-Agency Agreements & Institutional MOAs/MOUs",
    "Substantive Regulatory, Health & Penal Ordinances": "Substantive Regulatory, Health & Penal Ordinances",
    "Disaster Risk Reduction, Calamity & QRF Funds": "Substantive Regulatory, Health & Penal Ordinances"
}

def normalize_domain(raw_domain):
    return DOMAIN_MAP.get(raw_domain, "General Administration, Organization & Civil Service")

def get_era(year):
    if not year or year == 'N/A':
        return 'Unknown'
    try:
        y = int(year)
        if y < 1946:
            return 'Pre-War & Commonwealth (<1946)'
        elif y < 1986:
            return 'Third Republic & Martial Law (1946–1986)'
        elif y < 2016:
            return 'Fifth Republic & Decentralization (1987–2015)'
        else:
            return 'Modern Digital Era (2016–Present)'
    except:
        return 'Unknown'

def main():
    t_start = time.time()
    print("=" * 70)
    print("STEP 1: Ingesting Canonical Statutory Knowledge Graph Data")
    print("=" * 70)

    enactments = {}
    with open(NODES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            n = json.loads(line)
            if n.get('node_type') == 'enactment':
                enactments[n['id']] = n

    print(f"Loaded {len(enactments):,} enactments.")

    deg = Counter()
    edges = []
    G = nx.Graph()
    adj = defaultdict(set)

    with open(EDGES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            e = json.loads(line)
            rel = e.get('relation')
            if rel in ('CITES_AUTHORITY', 'AMENDS', 'REPEALS'):
                u, v = e['source'], e['target']
                if u in enactments and v in enactments:
                    deg[u] += 1
                    deg[v] += 1
                    t = 'cites' if rel == 'CITES_AUTHORITY' else ('amends' if rel == 'AMENDS' else 'repeals')
                    edges.append({'u': u, 'v': v, 't': t})
                    G.add_edge(u, v)
                    adj[u].add(v)
                    adj[v].add(u)

    print(f"Loaded {len(edges):,} relational edges across {len(deg):,} connected enactments.")

    # Find national laws directly cited by local ordinances (for Concentric View Shell 1)
    local_ordinances = {nid for nid, m in enactments.items() if m.get('jurisdiction') == 'local'}
    primary_national_anchors = set()
    for e in edges:
        u, v = e['u'], e['v']
        if u in local_ordinances and v not in local_ordinances:
            primary_national_anchors.add(v)
        elif v in local_ordinances and u not in local_ordinances:
            primary_national_anchors.add(u)

    print(f"Identified {len(primary_national_anchors):,} primary national statutory anchors directly cited by Davao ordinances.")

    print("\n" + "=" * 70)
    print("STEP 2: Precomputing Layout 1 — Force-Directed Organic Web (Spring Physics)")
    print("=" * 70)
    t0 = time.time()
    # Select connected core backbone (top 3,200 connected nodes + all connected local ordinances)
    core_candidates = sorted(deg.keys(), key=lambda x: deg[x], reverse=True)
    backbone_set = set(core_candidates[:2600])
    for nid in local_ordinances:
        if deg[nid] >= 1:
            backbone_set.add(nid)
    # Ensure flagship legal anchors are included
    for special in ('ra_7160_1991', 'pd_1096_1977', 'ra_9003_2001', 'ra_4136_1964', 'ra_1700_1957', 'ra_7636_1992', 'pd_958_1976'):
        if special in enactments:
            backbone_set.add(special)

    subG = G.subgraph(backbone_set)
    print(f"Computing spring physics on backbone of {subG.number_of_nodes():,} nodes ({subG.number_of_edges():,} edges)...")
    pos_backbone = nx.spring_layout(subG, k=0.18, iterations=45, weight=None, seed=42, scale=3600)
    print(f"Backbone spring layout calculated in {time.time() - t0:.2f}s!")

    coords_repulsion = {}
    for nid, (bx, by) in pos_backbone.items():
        coords_repulsion[nid] = (round(bx, 1), round(by, 1))

    # Place remaining connected nodes near their neighbors
    remaining_connected = [n for n in deg if n not in coords_repulsion]
    for nid in remaining_connected:
        neighbors = adj[nid]
        placed = False
        for nb in neighbors:
            if nb in coords_repulsion:
                nb_x, nb_y = coords_repulsion[nb]
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(70, 220)
                coords_repulsion[nid] = (round(nb_x + dist * math.cos(angle), 1), round(nb_y + dist * math.sin(angle), 1))
                placed = True
                break
        if not placed:
            # Place in intermediate organic ring
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(3400, 4200)
            coords_repulsion[nid] = (round(dist * math.cos(angle), 1), round(dist * math.sin(angle), 1))

    # Place isolated (degree 0) nodes in outer diffuse cosmic halo
    isolated_nodes = [nid for nid in enactments if nid not in coords_repulsion]
    for i, nid in enumerate(isolated_nodes):
        theta = i * 2.3999632  # Golden angle in radians
        r = 4200 + (i % 1200) + random.uniform(-60, 60)
        coords_repulsion[nid] = (round(r * math.cos(theta), 1), round(r * math.sin(theta), 1))

    print(f"Layout 1 (Repulsion Organic Web) complete for all {len(coords_repulsion):,} enactments.")

    print("\n" + "=" * 70)
    print("STEP 3: Precomputing Layout 2 — National Domain Topic Constellations (10 Galaxies)")
    print("=" * 70)
    # 10 Macro-Domain Galaxy Centers placed on an expansive ring (radius = 3,400)
    domain_galaxy_centers = {}
    R_GALAXY = 3400
    for idx, dom_name in enumerate(MACRO_DOMAINS):
        angle = (2 * math.pi * idx) / len(MACRO_DOMAINS) - (math.pi / 2)  # Start at 12 o'clock
        domain_galaxy_centers[dom_name] = (R_GALAXY * math.cos(angle), R_GALAXY * math.sin(angle))

    coords_domain = {}
    domain_node_counts = Counter()
    for nid, m in enactments.items():
        raw_dom = m.get('domain', 'General Administration, Organization & Civil Service')
        dom = normalize_domain(raw_dom)
        gx, gy = domain_galaxy_centers[dom]
        d = deg[nid]
        is_local = (m.get('jurisdiction') == 'local')
        idx = domain_node_counts[dom]
        domain_node_counts[dom] += 1

        theta = idx * 2.3999632
        if nid == 'ra_7160_1991':
            in_r = 15
        elif d >= 50:
            in_r = random.uniform(40, 180)
        elif d >= 10:
            in_r = random.uniform(180, 480)
        elif d >= 1:
            in_r = random.uniform(480, 850)
        else:
            in_r = random.uniform(850, 1250)

        # Local ordinances in that domain are slightly clustered as an azure satellite cluster
        if is_local:
            offset_x = 200 * math.cos(theta)
            offset_y = 200 * math.sin(theta)
            cx = gx + offset_x + in_r * 0.7 * math.cos(theta)
            cy = gy + offset_y + in_r * 0.7 * math.sin(theta)
        else:
            cx = gx + in_r * math.cos(theta)
            cy = gy + in_r * math.sin(theta)

        coords_domain[nid] = (round(cx, 1), round(cy, 1))

    print(f"Layout 2 (Domain Topic Constellations) complete for all {len(coords_domain):,} enactments.")

    print("\n" + "=" * 70)
    print("STEP 4: Precomputing Layout 3 — Vertical Preemption Hierarchy (Lex Superior)")
    print("=" * 70)
    # Columns along X-axis for each Macro-Domain (-4,500 to +4,500)
    col_width = 1000
    domain_col_centers = {}
    for idx, dom_name in enumerate(MACRO_DOMAINS):
        domain_col_centers[dom_name] = -4500 + idx * col_width

    coords_hierarchical = {}
    for nid, m in enactments.items():
        raw_dom = m.get('domain', 'General Administration, Organization & Civil Service')
        dom = normalize_domain(raw_dom)
        col_x = domain_col_centers[dom]
        is_local = (m.get('jurisdiction') == 'local')
        num_str = (m.get('number') or nid).upper()

        # Determine Vertical Tier (Y-coordinate)
        if nid in ('ra_7160_1991', 'eo_292_1987', 'act_3815_1930', 'ra_386_1949', 'ra_8424_1997'):
            # Tier 1 Apex: Supreme Framework Codes
            base_y = -2400
            y_jitter = random.uniform(-60, 60)
            x_jitter = random.uniform(-100, 100)
        elif is_local:
            # Tier 5 Floor: Davao City Local Ordinances
            base_y = 2400
            y_jitter = random.uniform(-400, 400)
            x_jitter = random.uniform(-420, 420)
        elif 'REPUBLIC ACT' in num_str or 'RA ' in num_str:
            # Tier 2: Republic Acts
            base_y = -1200
            y_jitter = random.uniform(-350, 350)
            x_jitter = random.uniform(-420, 420)
        elif any(k in num_str for k in ('PRESIDENTIAL DECREE', 'PD ', 'BATAS PAMBANSA', 'BP ', 'COMMONWEALTH ACT', 'CA ', 'ACT ')):
            # Tier 3: Decrees, Batas Pambansa & Commonwealth Acts
            base_y = 0
            y_jitter = random.uniform(-350, 350)
            x_jitter = random.uniform(-420, 420)
        elif 'EXECUTIVE ORDER' in num_str or 'EO ' in num_str:
            # Tier 4: Executive Orders
            base_y = 1100
            y_jitter = random.uniform(-300, 300)
            x_jitter = random.uniform(-420, 420)
        else:
            base_y = 500
            y_jitter = random.uniform(-300, 300)
            x_jitter = random.uniform(-420, 420)

        cx = col_x + x_jitter
        cy = base_y + y_jitter
        coords_hierarchical[nid] = (round(cx, 1), round(cy, 1))

    print(f"Layout 3 (Vertical Preemption Hierarchy) complete for all {len(coords_hierarchical):,} enactments.")

    print("\n" + "=" * 70)
    print("STEP 5: Precomputing Layout 4 — Concentric Planetary Orbits (RA 7160 Core)")
    print("=" * 70)
    coords_concentric = {}
    local_framework_ordinances = {
        'ord_0291_17', 'ord_0546_13', 'ord_0334_12', 'ord_0309_07', 'ord_0092_00', 'ord_0158_05', 'ord_0325_15'
    }

    concentric_counts = Counter()
    for nid, m in enactments.items():
        is_local = (m.get('jurisdiction') == 'local')
        raw_dom = m.get('domain', 'General Administration, Organization & Civil Service')
        dom = normalize_domain(raw_dom)
        dom_idx = MACRO_DOMAINS.index(dom)
        base_angle = (2 * math.pi * dom_idx) / len(MACRO_DOMAINS)

        if nid == 'ra_7160_1991':
            # Ring 0: Center Sun
            cx, cy = 0.0, 0.0
        elif nid in primary_national_anchors:
            # Ring 1: Primary National Statutory Anchors directly cited by Davao Ordinances
            concentric_counts['ring1'] += 1
            idx = concentric_counts['ring1']
            theta = base_angle + random.uniform(-0.25, 0.25)
            r = random.uniform(650, 1050)
            cx = r * math.cos(theta)
            cy = r * math.sin(theta)
        elif nid in local_framework_ordinances or (is_local and deg[nid] >= 8):
            # Ring 2: Major Davao City Regulatory Framework Ordinances
            concentric_counts['ring2'] += 1
            theta = base_angle + random.uniform(-0.25, 0.25)
            r = random.uniform(1500, 2050)
            cx = r * math.cos(theta)
            cy = r * math.sin(theta)
        elif is_local:
            # Ring 3: All other Davao City Local Ordinances
            concentric_counts['ring3'] += 1
            theta = base_angle + random.uniform(-0.28, 0.28)
            r = random.uniform(2400, 3100)
            cx = r * math.cos(theta)
            cy = r * math.sin(theta)
        else:
            # Ring 4: Outer Cosmic Halo of all remaining national laws
            concentric_counts['ring4'] += 1
            idx = concentric_counts['ring4']
            theta = idx * 2.3999632
            r = random.uniform(3600, 4800)
            cx = r * math.cos(theta)
            cy = r * math.sin(theta)

        coords_concentric[nid] = (round(cx, 1), round(cy, 1))

    print(f"Layout 4 (Concentric Planetary Orbits) complete for all {len(coords_concentric):,} enactments.")

    print("\n" + "=" * 70)
    print("STEP 6: Precomputing Layout 5 — Polar / Radial Wedges (Centrality Fan)")
    print("=" * 70)
    coords_radial = {}
    for nid, m in enactments.items():
        raw_dom = m.get('domain', 'General Administration, Organization & Civil Service')
        dom = normalize_domain(raw_dom)
        dom_idx = MACRO_DOMAINS.index(dom)
        base_angle = (2 * math.pi * dom_idx) / len(MACRO_DOMAINS)
        d = deg[nid]
        is_local = (m.get('jurisdiction') == 'local')

        angle_jitter = random.uniform(-0.20, 0.20)
        final_angle = base_angle + angle_jitter

        if nid == 'ra_7160_1991':
            r = 50
        elif is_local:
            r = random.uniform(350, 1600) if d > 0 else random.uniform(1600, 2400)
        elif d >= 50:
            r = random.uniform(150, 900)
        elif d >= 10:
            r = random.uniform(850, 1900)
        elif d >= 1:
            r = random.uniform(1700, 2900)
        else:
            r = random.uniform(2900, 3900)

        cx = r * math.cos(final_angle)
        cy = r * math.sin(final_angle)
        coords_radial[nid] = (round(cx, 1), round(cy, 1))

    print(f"Layout 5 (Polar / Radial Wedges) complete for all {len(coords_radial):,} enactments.")

    print("\n" + "=" * 70)
    print("STEP 7: Packaging Multi-Layout Node Payloads")
    print("=" * 70)
    nodes_payload = []
    for nid, m in enactments.items():
        d = deg[nid]
        is_local = (m.get('jurisdiction') == 'local')
        raw_dom = m.get('domain', 'General Administration, Organization & Civil Service')
        dom = normalize_domain(raw_dom)
        base_color = DOMAIN_PALETTE.get(dom, '#38BDF8')
        num_str = m.get('number', nid)

        # Instrument Classification
        inst_type = 'OTHER'
        if is_local:
            inst_type = 'ORD'
        else:
            u_num = num_str.upper()
            if 'REPUBLIC ACT' in u_num or 'RA ' in u_num:
                inst_type = 'RA'
            elif 'PRESIDENTIAL DECREE' in u_num or 'PD ' in u_num:
                inst_type = 'PD'
            elif 'BATAS PAMBANSA' in u_num or 'BP ' in u_num:
                inst_type = 'BP'
            elif 'EXECUTIVE ORDER' in u_num or 'EO ' in u_num:
                inst_type = 'EO'
            elif 'COMMONWEALTH ACT' in u_num or 'CA ' in u_num:
                inst_type = 'CA'
            elif 'ACT NO' in u_num or 'ACT ' in u_num:
                inst_type = 'ACT'

        label = num_str
        if len(label) > 24:
            label = label[:22] + '..'

        year = m.get('year', 'N/A')
        era = get_era(year)

        if nid == 'ra_7160_1991':
            r_val = 36
            c_val = '#FFD700'
            label = 'RA 7160 (Local Government Code)'
        elif d >= 50:
            r_val = min(24, max(12, int(8 + (d ** 0.5) * 1.5)))
            c_val = '#FFB300' if not is_local else '#00F2FE'
        elif d >= 15:
            r_val = min(14, max(7, int(5 + (d ** 0.5) * 1.2)))
            c_val = base_color if not is_local else '#00F2FE'
        elif is_local:
            r_val = min(10, max(4, int(3 + (d ** 0.5) * 1.0)))
            c_val = '#00F2FE'
        elif d >= 1:
            r_val = min(7, max(3, int(2.2 + (d ** 0.5) * 0.7)))
            c_val = base_color
        else:
            r_val = 2
            c_val = base_color

        # Default initial view: Organic Repulsion Web
        init_x, init_y = coords_repulsion[nid]

        nodes_payload.append({
            'id': nid,
            'x': init_x,
            'y': init_y,
            'xr': coords_repulsion[nid][0],
            'yr': coords_repulsion[nid][1],
            'xd': coords_domain[nid][0],
            'yd': coords_domain[nid][1],
            'xh': coords_hierarchical[nid][0],
            'yh': coords_hierarchical[nid][1],
            'xc': coords_concentric[nid][0],
            'yc': coords_concentric[nid][1],
            'xw': coords_radial[nid][0],
            'yw': coords_radial[nid][1],
            'r': r_val,
            'c': c_val,
            'label': label,
            'deg': d,
            'jur': 'local' if is_local else 'national',
            'type': inst_type,
            'num': num_str,
            'year': year,
            'era': era,
            'dom': dom,
            'raw_dom': raw_dom,
            'title': (m.get('title') or '')[:180]
        })

    print(f"Generated multi-layout payload with {len(nodes_payload):,} nodes and {len(edges):,} edges.")

    print("\n" + "=" * 70)
    print("STEP 8: Injecting Multi-Layout Support into statutory_kg_full_web.html")
    print("=" * 70)

    with open(OUTPUT_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update NODES and EDGES constants
    idx_nodes = html.find('const NODES = ')
    idx_nodes_end = html.find(';\n', idx_nodes) + 1
    html = html[:idx_nodes] + f'const NODES = {json.dumps(nodes_payload)};' + html[idx_nodes_end:]

    idx_edges = html.find('const EDGES = ')
    idx_edges_end = html.find(';\n', idx_edges) + 1
    html = html[:idx_edges] + f'const EDGES = {json.dumps(edges)};' + html[idx_edges_end:]

    # Write the updated HTML
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Injected updated datasets into {OUTPUT_HTML} (Size: {os.path.getsize(OUTPUT_HTML) / (1024*1024):.2f} MB)")
    print(f"Total time elapsed: {time.time() - t_start:.2f}s")
    print("=" * 70)

if __name__ == '__main__':
    main()

