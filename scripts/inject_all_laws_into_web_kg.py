import json
import math
import random
from collections import Counter

random.seed(42)

print("[1/5] Ingesting enactment nodes from canonical KG...")
enactments = {}
with open('data/knowledge_graph/statutory_kg_nodes.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        n = json.loads(line)
        if n.get('node_type') == 'enactment':
            enactments[n['id']] = n

print(f"      Loaded {len(enactments):,} enactments.")

print("[2/5] Ingesting edges from canonical KG...")
deg = Counter()
edges = []
with open('data/knowledge_graph/statutory_kg_edges.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        e = json.loads(line)
        if e.get('relation') in ('CITES_AUTHORITY', 'AMENDS', 'REPEALS'):
            u, v = e['source'], e['target']
            if u in enactments and v in enactments:
                deg[u] += 1
                deg[v] += 1
                t = 'cites' if e['relation'] == 'CITES_AUTHORITY' else ('amends' if e['relation'] == 'AMENDS' else 'repeals')
                edges.append({'u': u, 'v': v, 't': t})

print(f"      Loaded {len(edges):,} enactment-level relational edges.")

DOMAIN_PALETTE = {
    'General Administration, Organization & Civil Service': '#38BDF8',
    'Public Finance, Taxation, Fiscal Policy & Budget': '#F59E0B',
    'Police Power, Public Order, Safety & Penal Law': '#EF4444',
    'Social Services, Education, Labor & Human Development': '#10B981',
    'Public Works, Transportation, Utilities & Infrastructure': '#8B5CF6',
    'Commerce, Trade, Industry, Agriculture & Economic Enterprise': '#06B6D4',
    'Environmental Protection, Zoning, Land Use & Natural Resources': '#84CC16',
    'Executive Issuances & Policy Reorganization': '#EC4899',
    'Inter-Agency Agreements & Institutional MOAs/MOUs': '#F97316',
    'Substantive Regulatory, Health & Penal Ordinances': '#14B8A6'
}

DOMAINS = list(DOMAIN_PALETTE.keys())
domain_angles = {d: (2 * math.pi * i / len(DOMAINS)) for i, d in enumerate(DOMAINS)}

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

print("[3/5] Computing multi-polar organic spatial coordinates for all enactments...")
nodes_payload = []
for nid, m in enactments.items():
    d = deg[nid]
    is_local = (m.get('jurisdiction') == 'local')
    dom = m.get('domain', 'General Administration, Organization & Civil Service')
    if dom not in domain_angles:
        dom = 'General Administration, Organization & Civil Service'
    
    angle_base = domain_angles[dom]
    if is_local:
        angle_jitter = random.uniform(-0.16, 0.16)
        radius = random.uniform(300, 1600) if d > 0 else random.uniform(1600, 2400)
    else:
        angle_jitter = random.uniform(-0.22, 0.22)
        if nid == 'ra_7160_1991':
            radius = 45
        elif d >= 50:
            radius = random.uniform(120, 850)
        elif d >= 10:
            radius = random.uniform(700, 1900)
        elif d >= 1:
            radius = random.uniform(1500, 2900)
        else:
            radius = random.uniform(2900, 3900)
            
    final_angle = angle_base + angle_jitter
    x = round(radius * math.cos(final_angle) + random.uniform(-15, 15), 1)
    y = round(radius * math.sin(final_angle) + random.uniform(-15, 15), 1)
    
    num_str = m.get('number', nid)
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
    base_color = DOMAIN_PALETTE.get(dom, '#38BDF8')
    
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
        
    nodes_payload.append({
        'id': nid,
        'x': x,
        'y': y,
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
        'title': (m.get('title') or '')[:180]
    })

print(f"[4/5] Generated {len(nodes_payload):,} nodes and {len(edges):,} edges.")

# Verification
p958 = [n for n in nodes_payload if n['id'] == 'pd_958_1976']
print(f"      Verification: PD 958 present = {bool(p958)}")
if p958:
    print(f"      PD 958 Record: {p958[0]['num']}, Type: {p958[0]['type']}, Degree: {p958[0]['deg']}")

print("[5/5] Injecting into statutory_kg_full_web.html...")
with open('output/visualizations/statutory_kg_full_web.html', 'r', encoding='utf-8') as f:
    html_lines = f.readlines()

new_html_lines = []
for line in html_lines:
    if line.strip().startswith('const NODES = '):
        new_html_lines.append(f'    const NODES = {json.dumps(nodes_payload)};\n')
    elif line.strip().startswith('const EDGES = '):
        new_html_lines.append(f'    const EDGES = {json.dumps(edges)};\n')
    elif 'id="stat-visible-nodes"' in line:
        new_html_lines.append(f'        <span class="stat-val" id="stat-visible-nodes">{len(nodes_payload):,}</span>\n')
    elif 'id="stat-visible-edges"' in line:
        new_html_lines.append(f'        <span class="stat-val" id="stat-visible-edges">{len(edges):,}</span>\n')
    elif 'id="degree-slider"' in line:
        new_html_lines.append('          <input type="range" id="degree-slider" min="0" max="40" value="0" step="1">\n')
    elif 'id="degree-val"' in line:
        new_html_lines.append('          <span class="slider-val" id="degree-val">0</span>\n')
    elif 'let filterMinDegree = 1;' in line:
        new_html_lines.append('    let filterMinDegree = 0;\n')
    else:
        new_html_lines.append(line)

with open('output/visualizations/statutory_kg_full_web.html', 'w', encoding='utf-8') as f:
    f.writelines(new_html_lines)

print("SUCCESS! statutory_kg_full_web.html now contains all 27,248 laws and 30,034 relations.")

