import json
import networkx as nx
from pathlib import Path

# Load KG
G = nx.Graph()
print("[*] Ingesting KG edges...")
with open("data/knowledge_graph/statutory_kg_edges.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        e = json.loads(line)
        u = e["source"].lower()
        v = e["target"].lower()
        rel = e.get("relation", "")
        G.add_edge(u, v, relation=rel)

print(f"[*] KG Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")

# Load Benchmark cases
cases = []
with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            cases.append(json.loads(line))

# Map cases to node IDs
# Let's see node IDs in G
CASE_NODES = [
    ("DAVAO-TIER3-01", "davao_ordinance_no_0309_07", "pd_1144_1977"),
    ("DAVAO-TIER3-02", "davao_ordinance_no_092_00", "ra_7160_1991"),
    ("DAVAO-TIER3-03", "davao_ordinance_no_0158_05", "ra_7160_1991"),
    ("DAVAO-TIER3-04", "davao_ordinance_no_0158_05", "ra_7160_1991"),
    ("DAVAO-TIER3-05", "davao_ordinance_no_0158_05", "ra_7160_1991"),
    ("DAVAO-TIER3-06", "davao_ordinance_no_0325_15", "ra_7942_1995"),
    ("DAVAO-TIER3-07", "davao_ordinance_no_0367_12", "ra_7160_1991"),
    ("DAVAO-TIER3-08", "davao_ordinance_no_0270_23", "ra_4136_1964"),
    ("SC-PHIL-09", "cdo_ordinance_no_3375_93", "pd_1869_1983"),
    ("SC-PHIL-10", "manila_ordinance_no_7783_93", "ph_const_1987"),
]

print("\n" + "="*80)
print("COMPUTING TOPOLOGICAL SHORTEST-PATH DISTANCES IN STATUTORY KNOWLEDGE GRAPH")
print("="*80)

for cid, ord_node, stat_node in CASE_NODES:
    has_ord = ord_node in G
    has_stat = stat_node in G
    dist = None
    if has_ord and has_stat:
        try:
            dist = nx.shortest_path_length(G, ord_node, stat_node)
            path = nx.shortest_path(G, ord_node, stat_node)
        except nx.NetworkXNoPath:
            dist = float('inf')
            path = []
    print(f"{cid:<15} | Ord in G: {str(has_ord):<5} | Stat in G: {str(has_stat):<5} | d_G: {dist}")
    if dist and dist != float('inf'):
        print(f"  Path: {' -> '.join(path)}")

