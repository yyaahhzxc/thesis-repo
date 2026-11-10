import json

with open('output/knowledge_graph/statutory_kg_summary.json', 'r', encoding='utf-8') as f:
    res = json.load(f)

print('=== EXPERIMENT 1: TOP SUPER-HUBS & PAGERANK ===')
print('Top 10 Overall Super-Hubs in Positive Law:')
for h in res['experiment_1_super_hubs']['top_overall_super_hubs'][:10]:
    t = h['title'][:60].replace('\n', ' ')
    print(f"  Rank {h['rank']:2d}: {h['number']} ({h['jurisdiction'].upper()}, {h['year']}) | In-Deg: {h['in_degree']:4d} | PR: {h['pagerank']:.6f} | {t}")

print('\nTop 10 Authorities Cited by Davao City Ordinances:')
for h in res['experiment_1_super_hubs']['top_davao_authorities'][:10]:
    t = h['title'][:60].replace('\n', ' ')
    print(f"  Rank {h['rank']:2d}: {h['number']} ({h['year']}) | Davao Cites: {h['davao_citations']:4d} | PR: {h['pagerank']:.6f} | {t}")

print('\n=== EXPERIMENT 2: SCALE-FREE POWER-LAW FIT ===')
exp2 = res['experiment_2_scale_free']
print(f"  Scaling exponent (gamma): {exp2['scaling_exponent_gamma']}")
print(f"  R^2 goodness-of-fit:     {exp2['r2_goodness_of_fit']}")
print(f"  Scale-Free Topology:     {exp2['is_scale_free']}")
print(f"  Max In-Degree:           {exp2['max_in_degree']}")

print('\n=== EXPERIMENT 3: LOUVAIN COMMUNITY DETECTION ===')
exp3 = res['experiment_3_louvain']
print(f"  Total Communities:       {exp3['total_communities_detected']}")
print(f"  Modularity (Q):          {exp3['modularity_q']}")
print(f"  High Modularity (>0.40): {exp3['high_modularity_confirmed']}")
print('  Top Communities:')
for c in exp3['top_10_communities'][:5]:
    print(f"    Comm {c['community_id']:2d}: Size={c['size']:4d} | Dominant: '{c['dominant_domain']}' ({c['domain_purity_pct']}%) | Nat={c['national_enactments']}, Local={c['local_ordinances']}")

print('\n=== EXPERIMENT 4: GLOBAL CONNECTIVITY (GCC & ORPHANS) ===')
exp4 = res['experiment_4_connectivity']
print(f"  Total Enactments:        {exp4['total_enactments']}")
print(f"  GCC Size:                {exp4['gcc_size']} ({exp4['gcc_percentage']}%)")
print(f"  Local Ordinances in GCC: {exp4['local_ordinances_in_gcc']} / {exp4['total_local_ordinances']} ({exp4['local_integration_rate_pct']}%)")
print(f"  Orphan Enactments:       {exp4['orphan_nodes_count']} ({exp4['orphan_nodes_pct']}%) [Local: {exp4['orphan_local_count']}, Nat: {exp4['orphan_national_count']}]")
print(f"  Top Orphan Typologies:   {exp4['top_orphan_local_typologies']}")

print('\n=== EXPERIMENT 5: DAG LINEAGE & AMENDATORY DEPTH ===')
exp5 = res['experiment_5_lineage_dag']
print(f"  Amendatory Nodes:        {exp5['total_amendatory_nodes']}")
print(f"  Amendatory Edges:        {exp5['total_amendatory_edges']}")
print(f"  Strictly Acyclic DAG:    {exp5['is_strictly_acyclic_dag']}")
print(f"  Detected Cycles:         {exp5['detected_cycle_count']}")
print(f"  Max Amendatory Depth:    {exp5['max_amendatory_chain_depth']}")
print('  Longest Amendatory Lineage Path:')
for node in exp5['longest_amendatory_lineage']:
    t = node['title'][:60].replace('\n', ' ')
    print(f"    -> {node['number']} ({node['jurisdiction']}, {node['year']}): {t}")

