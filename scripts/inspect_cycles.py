import sys
sys.path.append('.')
import json
import networkx as nx
from src.knowledge_graph.build_statutory_kg import build_alias_registry, extract_edges

enactment_meta, alias_to_id = build_alias_registry()
edges_cites, edges_amends, edges_repeals = extract_edges(enactment_meta, alias_to_id)

G_amend = nx.DiGraph()
for u, v in edges_amends:
    G_amend.add_edge(u, v, rel='AMENDS')
for u, v in edges_repeals:
    G_amend.add_edge(u, v, rel='REPEALS')

cycles = list(nx.simple_cycles(G_amend))
print(f"Total cycles detected: {len(cycles)}")
for i, c in enumerate(cycles[:10], 1):
    print(f"\nCycle {i} (length {len(c)}):")
    for node in c:
        m = enactment_meta.get(node, {})
        num = m.get('number', node)
        jur = m.get('jurisdiction', '')
        yr = m.get('year', '')
        print(f"  [{node}] {num} ({jur}, {yr})")
