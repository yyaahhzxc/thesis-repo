import networkx as nx
import time
import sys

t0 = time.time()
G = nx.DiGraph()

# Add 27,357 enactment nodes
for i in range(27357):
    G.add_node(f"enact_{i}", node_type="enactment")

# Add 178,494 provision nodes
for i in range(178494):
    G.add_node(f"prov_{i}", node_type="provision")
    # CONTAINS edge
    G.add_edge(f"enact_{i % 27357}", f"prov_{i}", relation="CONTAINS")

# Add 50,000 citation/amend edges between enactments
import random
random.seed(42)
for _ in range(50000):
    u = f"enact_{random.randint(0, 27356)}"
    v = f"enact_{random.randint(0, 27356)}"
    if u != v:
        G.add_edge(u, v, relation="CITES_AUTHORITY")

t1 = time.time()
print(f"Graph built in {t1-t0:.2f}s!")
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# Test degree centrality
t2 = time.time()
# compute in-degree on enactment subgraph
sub = nx.subgraph_view(G, filter_node=lambda n: G.nodes[n].get("node_type") == "enactment")
in_deg = dict(sub.in_degree())
top5 = sorted(in_deg.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"Top in-degrees on sub in {time.time()-t2:.2f}s: {top5}")

# Test PageRank on enactment sub-graph
t3 = time.time()
# Create DiGraph of just enactments for PageRank
G_enact = nx.DiGraph()
for u, v, d in G.edges(data=True):
    if d.get("relation") == "CITES_AUTHORITY":
        G_enact.add_edge(u, v)

pr = nx.pagerank(G_enact, alpha=0.85, max_iter=50)
print(f"PageRank computed on {G_enact.number_of_nodes()} nodes in {time.time()-t3:.2f}s!")

