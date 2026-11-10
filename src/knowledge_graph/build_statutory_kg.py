"""
build_statutory_kg.py
=====================
Constructs the Multi-Relational Statutory Knowledge Graph across Philippine
national statutes (25,432 enactments) and Davao City local ordinances (1,925 enactments)
alongside 178,494 granular statutory provisions and 8 macro legal domains.

Graph Schema: G = (V, E, R)
Relation Vocabulary:
  - CONTAINS: Enactment -> Provision
  - GOVERNS_DOMAIN: Domain -> Enactment / Provision
  - CITES_AUTHORITY: Source Enactment -> Target Enactment
  - AMENDS: Amending Enactment -> Predecessor Enactment
  - REPEALS: Repealing Enactment -> Repealed Enactment

Executes 5 Standalone Topological Experiments:
  1. In-Degree Centrality & Statutory PageRank (Super-Hub Analysis)
  2. Scale-Free Power-Law Degree Distribution Goodness of Fit (R^2, gamma)
  3. Louvain Community Detection & Modularity (Q)
  4. Global Connectivity Audit (Giant Connected Component & Orphan Analysis)
  5. Directed Acyclic Graph (DAG) Cycle Detection & Amendatory Lineage Depth
"""

import json
import os
import re
import time
import math
from collections import Counter, defaultdict
import numpy as np
import networkx as nx

# Define paths
CORPUS_NATIONAL = "corpus/cleaned/national/categorized_national_laws.jsonl"
CORPUS_LOCAL = "corpus/city_ordinances/categorized_davao_ordinances.jsonl"
UNIFIED_PROVISIONS = "data/unified_dual_statutory_provisions.jsonl"
OUTPUT_DIR = "output/knowledge_graph"

MACRO_DOMAINS = [
    "General Administration, Organization & Civil Service",
    "Public Finance, Taxation, Fiscal Policy & Budget",
    "Police Power, Public Order, Safety & Penal Law",
    "Social Services, Education, Labor & Human Development",
    "Public Works, Transportation, Utilities & Infrastructure",
    "Commerce, Trade, Industry, Agriculture & Economic Enterprise",
    "Environmental Protection, Zoning, Land Use & Natural Resources",
    "Executive Issuances & Policy Reorganization"
]

def build_alias_registry():
    """
    Constructs canonical alias dictionaries mapping textual citation variants
    to unique Enactment IDs across both national and local legislation.
    """
    print("[1/6] Ingesting enactment metadata and building alias registry...")
    alias_to_id = {}
    enactment_meta = {}

    # 1. National Statutes (25,432 enactments)
    with open(CORPUS_NATIONAL, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            lid = data["law_id"]
            cat = data.get("category", "")
            lnum = data.get("law_number", "")
            year = data.get("year")
            domain = data.get("topic_label", "Executive Issuances & Policy Reorganization")

            enactment_meta[lid] = {
                "id": lid,
                "jurisdiction": "national",
                "number": lnum,
                "category": cat,
                "year": year,
                "title": data.get("long_title", ""),
                "domain": domain,
                "word_count": data.get("word_count", 0)
            }

            parts = lid.split("_")
            prefix = parts[0].lower()
            m = re.search(r'(\d+)', lnum)
            if m:
                num = int(m.group(1))
                alias_to_id[(prefix, num)] = lid

    # 2. Davao City Ordinances (1,925 enactments)
    with open(CORPUS_LOCAL, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            oid = data["ordinance_id"]
            onum = data.get("ordinance_number", "").strip().lower()
            year = data.get("year")
            typology = data.get("functional_typology", "Administrative Routine")

            enactment_meta[oid] = {
                "id": oid,
                "jurisdiction": "local",
                "number": onum,
                "category": "City Ordinance",
                "year": year,
                "title": data.get("title", ""),
                "domain": typology,
                "word_count": data.get("word_count", 0)
            }

            if onum:
                alias_to_id[("ord", onum)] = oid
                parts = onum.split("-")
                if len(parts) == 2:
                    p0 = str(int(parts[0])) if parts[0].isdigit() else parts[0]
                    alias_to_id[("ord", f"{p0}-{parts[1]}")] = oid

    print(f"      Ingested {len(enactment_meta)} enactments ({sum(1 for e in enactment_meta.values() if e['jurisdiction']=='national')} national, {sum(1 for e in enactment_meta.values() if e['jurisdiction']=='local')} local).")
    print(f"      Indexed {len(alias_to_id)} canonical citation resolution targets.")
    return enactment_meta, alias_to_id


def extract_edges(enactment_meta, alias_to_id):
    """
    Extracts multi-relational edges across all legislative enactments:
      - CITES_AUTHORITY
      - AMENDS
      - REPEALS
    Uses safe bounded text windowing around trigger tokens to eliminate backtracking.
    """
    print("[2/6] Extracting authority citations and amendatory lineages...")

    citation_patterns = [
        ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
        ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
        ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
        ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
        ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
        ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
        ("ord", re.compile(r'(?:City\s+Ordinance|Ordinance)\s+No\.?\s*([0-9]+(?:-[0-9]+)?)', re.IGNORECASE)),
    ]

    amend_trigger = re.compile(r'\b(?:hereby\s+amended|is\s+amended|are\s+amended|amending|as\s+amended\s+by)\b', re.IGNORECASE)
    repeal_trigger = re.compile(r'\b(?:hereby\s+repealed|is\s+repealed|are\s+repealed|repealing)\b', re.IGNORECASE)

    edges_cites = Counter()
    edges_amends = set()
    edges_repeals = set()

    def find_targets(text_segment):
        found = set()
        for prefix, pat in citation_patterns:
            for m in pat.finditer(text_segment):
                raw = m.group(1).lower()
                key = (prefix, int(raw) if prefix != "ord" else raw)
                tid = alias_to_id.get(key)
                if tid:
                    found.add(tid)
        return found

    t_start = time.time()

    # Process Local Ordinances
    with open(CORPUS_LOCAL, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            src_id = data["ordinance_id"]
            text = data.get("full_text", "")
            src_year = enactment_meta.get(src_id, {}).get("year") or 9999

            # Authority Citations
            targets = find_targets(text)
            for tid in targets:
                if tid != src_id:
                    edges_cites[(src_id, tid)] += 1

            # Lineage Amendments (under lex posterior, amending enactment must be chronologically posterior: src_year > tgt_year)
            for m in amend_trigger.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta.get(tid, {}).get("year") or 0
                        if src_year > tgt_year:
                            edges_amends.add((src_id, tid))

            # Lineage Repeals (src_year > tgt_year)
            for m in repeal_trigger.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta.get(tid, {}).get("year") or 0
                        if src_year > tgt_year:
                            edges_repeals.add((src_id, tid))

    # Process National Laws
    with open(CORPUS_NATIONAL, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            src_id = data["law_id"]
            text = data.get("full_text", "")
            src_year = enactment_meta.get(src_id, {}).get("year") or 9999

            # Authority Citations
            targets = find_targets(text)
            for tid in targets:
                if tid != src_id:
                    edges_cites[(src_id, tid)] += 1

            # Lineage Amendments (src_year > tgt_year)
            for m in amend_trigger.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta.get(tid, {}).get("year") or 0
                        if src_year > tgt_year:
                            edges_amends.add((src_id, tid))

            # Lineage Repeals (src_year > tgt_year)
            for m in repeal_trigger.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta.get(tid, {}).get("year") or 0
                        if src_year > tgt_year:
                            edges_repeals.add((src_id, tid))

    t_elapsed = time.time() - t_start
    print(f"      Extraction finished in {t_elapsed:.2f}s!")
    print(f"      - Directed CITES_AUTHORITY edges: {len(edges_cites):,} (occurrences: {sum(edges_cites.values()):,})")
    print(f"      - Directed AMENDS edges: {len(edges_amends):,}")
    print(f"      - Directed REPEALS edges: {len(edges_repeals):,}")

    return edges_cites, edges_amends, edges_repeals


def assemble_graph(enactment_meta, edges_cites, edges_amends, edges_repeals):
    """
    Assembles the heterogeneous directed NetworkX graph G = (V, E, R).
    """
    print("[3/6] Assembling NetworkX heterogeneous multi-relational graph...")
    G = nx.DiGraph()

    # 1. Enactment Nodes
    for eid, meta in enactment_meta.items():
        G.add_node(eid, node_type="enactment", **meta)

    # 2. Domain Hub Nodes
    for i, dname in enumerate(MACRO_DOMAINS):
        dhub_id = f"domain_{i}"
        G.add_node(dhub_id, node_type="domain", domain_name=dname)
        # Link enactments assigned to this domain
        for eid, meta in enactment_meta.items():
            if meta.get("domain") == dname:
                G.add_edge(dhub_id, eid, relation="GOVERNS_DOMAIN")

    # 3. Citation Edges
    for (u, v), weight in edges_cites.items():
        if G.has_node(u) and G.has_node(v):
            G.add_edge(u, v, relation="CITES_AUTHORITY", weight=weight)

    # 4. Amendatory Edges
    for (u, v) in edges_amends:
        if G.has_node(u) and G.has_node(v):
            G.add_edge(u, v, relation="AMENDS")

    # 5. Repealing Edges
    for (u, v) in edges_repeals:
        if G.has_node(u) and G.has_node(v):
            G.add_edge(u, v, relation="REPEALS")

    print(f"      Total Graph Vertices: {G.number_of_nodes():,}")
    print(f"      Total Graph Edges: {G.number_of_edges():,}")
    return G


def run_topological_experiments(G, enactment_meta):
    """
    Executes the 5 topological experiments from §3.7.4.3 & §3.9.3:
      Exp 1: In-Degree Centrality & Statutory PageRank (Super-Hub Analysis)
      Exp 2: Scale-Free Power-Law Degree Distribution (R^2, gamma)
      Exp 3: Louvain Community Detection & Modularity (Q)
      Exp 4: Global Connectivity Audit (GCC & Orphan Analysis)
      Exp 5: Directed Acyclic Graph (DAG) Cycle Detection & Amendatory Lineages
    """
    print("[4/6] Executing 5 standalone topological experiments on graph topology...")
    results = {}

    # Isolate enactment citation subgraph for clean topological analysis
    G_cite = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "CITES_AUTHORITY":
            G_cite.add_edge(u, v, weight=d.get("weight", 1))

    # Ensure all enactments exist in G_cite (even if isolated)
    for eid in enactment_meta:
        if not G_cite.has_node(eid):
            G_cite.add_node(eid)

    N_enact = len(enactment_meta)

    # -------------------------------------------------------------
    # Experiment 1: Centrality & Statutory PageRank (Super-Hubs)
    # -------------------------------------------------------------
    print("      -> Experiment 1: Centrality & Statutory PageRank...")
    in_degrees = dict(G_cite.in_degree())
    norm_in_degrees = {k: v / (N_enact - 1) for k, v in in_degrees.items()}

    t_pr = time.time()
    pr_scores = nx.pagerank(G_cite, alpha=0.85, max_iter=100, tol=1e-6)
    t_pr_elapsed = time.time() - t_pr

    # Top 20 overall super-hubs
    top_in_deg = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:20]
    top_pr = sorted(pr_scores.items(), key=lambda x: x[1], reverse=True)[:20]

    top_super_hubs = []
    for rank, (eid, indeg) in enumerate(top_in_deg, 1):
        meta = enactment_meta.get(eid, {})
        top_super_hubs.append({
            "rank": rank,
            "id": eid,
            "number": meta.get("number", eid),
            "jurisdiction": meta.get("jurisdiction", "unknown"),
            "year": meta.get("year"),
            "title": meta.get("title", "")[:100],
            "in_degree": indeg,
            "norm_in_degree": round(norm_in_degrees[eid], 6),
            "pagerank": round(pr_scores.get(eid, 0.0), 6)
        })

    # Citations specifically from Davao City Ordinances to National Statutes
    davao_to_nat_citations = Counter()
    for u, v, d in G.edges(data=True):
        if d.get("relation") == "CITES_AUTHORITY":
            u_meta = enactment_meta.get(u, {})
            v_meta = enactment_meta.get(v, {})
            if u_meta.get("jurisdiction") == "local" and v_meta.get("jurisdiction") == "national":
                davao_to_nat_citations[v] += d.get("weight", 1)

    top_davao_authorities = []
    for rank, (eid, count) in enumerate(davao_to_nat_citations.most_common(15), 1):
        meta = enactment_meta.get(eid, {})
        top_davao_authorities.append({
            "rank": rank,
            "id": eid,
            "number": meta.get("number", eid),
            "year": meta.get("year"),
            "title": meta.get("title", "")[:100],
            "davao_citations": count,
            "pagerank": round(pr_scores.get(eid, 0.0), 6)
        })

    results["experiment_1_super_hubs"] = {
        "pagerank_runtime_seconds": round(t_pr_elapsed, 3),
        "top_overall_super_hubs": top_super_hubs,
        "top_davao_authorities": top_davao_authorities
    }

    # -------------------------------------------------------------
    # Experiment 2: Scale-Free Power-Law Degree Distribution
    # -------------------------------------------------------------
    print("      -> Experiment 2: Scale-Free Power-Law Degree Distribution...")
    degree_counts = Counter([deg for deg in in_degrees.values() if deg > 0])
    k_vals = np.array(sorted(degree_counts.keys()))
    pk_vals = np.array([degree_counts[k] / N_enact for k in k_vals])

    # Fit log-log linear regression: ln(P(k)) = -gamma * ln(k) + c
    log_k = np.log(k_vals)
    log_pk = np.log(pk_vals)

    # Linear least squares
    slope, intercept = np.polyfit(log_k, log_pk, 1)
    gamma = -slope
    y_pred = slope * log_k + intercept

    # Coefficient of determination R^2
    ss_res = np.sum((log_pk - y_pred) ** 2)
    ss_tot = np.sum((log_pk - np.mean(log_pk)) ** 2)
    r2_power_law = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    results["experiment_2_scale_free"] = {
        "scaling_exponent_gamma": round(float(gamma), 4),
        "r2_goodness_of_fit": round(float(r2_power_law), 4),
        "is_scale_free": bool(r2_power_law >= 0.85 and 1.5 <= gamma <= 3.5),
        "max_in_degree": int(np.max(k_vals)) if len(k_vals) > 0 else 0,
        "degrees_evaluated_count": len(k_vals)
    }

    # -------------------------------------------------------------
    # Experiment 3: Louvain Community Detection & Modularity
    # -------------------------------------------------------------
    print("      -> Experiment 3: Louvain Community Detection & Modularity...")
    G_undir = G_cite.to_undirected()
    # Retain non-trivial connected nodes
    connected_nodes = [n for n in G_undir.nodes() if G_undir.degree(n) > 0]
    G_sub_undir = G_undir.subgraph(connected_nodes)

    t_louv = time.time()
    communities = nx.community.louvain_communities(G_sub_undir, seed=42)
    t_louv_elapsed = time.time() - t_louv
    q_modularity = nx.community.modularity(G_sub_undir, communities)

    community_profiles = []
    for c_id, comm in enumerate(sorted(communities, key=len, reverse=True)[:10], 1):
        comm_domains = Counter([enactment_meta[n].get("domain") for n in comm if n in enactment_meta])
        comm_jurisdictions = Counter([enactment_meta[n].get("jurisdiction") for n in comm if n in enactment_meta])
        top_domain = comm_domains.most_common(1)[0] if comm_domains else ("Unknown", 0)
        purity = (top_domain[1] / len(comm)) * 100 if len(comm) > 0 else 0.0

        community_profiles.append({
            "community_id": c_id,
            "size": len(comm),
            "dominant_domain": top_domain[0],
            "domain_purity_pct": round(purity, 2),
            "national_enactments": comm_jurisdictions.get("national", 0),
            "local_ordinances": comm_jurisdictions.get("local", 0)
        })

    results["experiment_3_louvain"] = {
        "runtime_seconds": round(t_louv_elapsed, 3),
        "total_communities_detected": len(communities),
        "modularity_q": round(float(q_modularity), 4),
        "high_modularity_confirmed": bool(q_modularity > 0.40),
        "top_10_communities": community_profiles
    }

    # -------------------------------------------------------------
    # Experiment 4: Global Connectivity Audit (GCC & Orphans)
    # -------------------------------------------------------------
    print("      -> Experiment 4: Global Connectivity Audit (GCC & Orphans)...")
    wccs = list(nx.weakly_connected_components(G_cite))
    gcc = max(wccs, key=len) if wccs else set()
    gcc_size = len(gcc)
    gcc_pct = (gcc_size / N_enact) * 100

    # Local ordinances in GCC
    local_in_gcc = sum(1 for n in gcc if enactment_meta[n]["jurisdiction"] == "local")
    total_local = sum(1 for n in enactment_meta.values() if n["jurisdiction"] == "local")
    local_gcc_pct = (local_in_gcc / total_local) * 100 if total_local > 0 else 0.0

    # Orphan nodes (in-degree = 0 and out-degree = 0)
    orphans = [n for n in G_cite.nodes() if G_cite.in_degree(n) == 0 and G_cite.out_degree(n) == 0]
    orphan_local = [n for n in orphans if enactment_meta[n]["jurisdiction"] == "local"]
    orphan_national = [n for n in orphans if enactment_meta[n]["jurisdiction"] == "national"]

    # Sample orphan local typologies
    orphan_local_domains = Counter([enactment_meta[n].get("domain") for n in orphan_local])

    results["experiment_4_connectivity"] = {
        "total_enactments": N_enact,
        "total_connected_components": len(wccs),
        "gcc_size": gcc_size,
        "gcc_percentage": round(gcc_pct, 2),
        "local_ordinances_in_gcc": local_in_gcc,
        "total_local_ordinances": total_local,
        "local_integration_rate_pct": round(local_gcc_pct, 2),
        "orphan_nodes_count": len(orphans),
        "orphan_nodes_pct": round((len(orphans) / N_enact) * 100, 2),
        "orphan_local_count": len(orphan_local),
        "orphan_national_count": len(orphan_national),
        "top_orphan_local_typologies": dict(orphan_local_domains.most_common(5))
    }

    # -------------------------------------------------------------
    # Experiment 5: DAG Cycle Detection & Amendatory Lineage Depth
    # -------------------------------------------------------------
    print("      -> Experiment 5: DAG Lineage Validation & Amendatory Chains...")
    G_amend = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        if d.get("relation") in ["AMENDS", "REPEALS"]:
            G_amend.add_edge(u, v, relation=d.get("relation"))

    is_dag = nx.is_directed_acyclic_graph(G_amend)
    cycles = list(nx.simple_cycles(G_amend)) if not is_dag else []

    longest_path_len = 0
    longest_path_nodes = []
    if is_dag and G_amend.number_of_nodes() > 0:
        longest_path_len = nx.dag_longest_path_length(G_amend)
        longest_path_nodes = nx.dag_longest_path(G_amend)

    longest_lineage_details = []
    for eid in longest_path_nodes:
        meta = enactment_meta.get(eid, {})
        longest_lineage_details.append({
            "id": eid,
            "number": meta.get("number", eid),
            "year": meta.get("year"),
            "jurisdiction": meta.get("jurisdiction", ""),
            "title": meta.get("title", "")[:80]
        })

    results["experiment_5_lineage_dag"] = {
        "total_amendatory_nodes": G_amend.number_of_nodes(),
        "total_amendatory_edges": G_amend.number_of_edges(),
        "is_strictly_acyclic_dag": is_dag,
        "detected_cycle_count": len(cycles),
        "max_amendatory_chain_depth": longest_path_len,
        "longest_amendatory_lineage": longest_lineage_details
    }

    return results


def link_provisions(G):
    """
    Ingests granular provisions from unified_dual_statutory_provisions.jsonl
    and connects them to parent enactments via CONTAINS edges.
    """
    print("[5/6] Ingesting and linking granular statutory provisions (178,494 provisions)...")
    t_start = time.time()
    prov_count = 0
    attached_count = 0

    with open(UNIFIED_PROVISIONS, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            pid = data["provision_id"]
            eid = data["enactment_id"]

            G.add_node(pid,
                node_type="provision",
                section_number=data.get("section_number", ""),
                is_operative=data.get("is_operative", True),
                is_boilerplate=data.get("is_boilerplate", False),
                est_tokens=data.get("est_tokens", 0),
                jurisdiction=data.get("jurisdiction", "national")
            )
            prov_count += 1

            if G.has_node(eid):
                G.add_edge(eid, pid, relation="CONTAINS")
                attached_count += 1

    t_elapsed = time.time() - t_start
    print(f"      Linked {prov_count:,} provisions ({attached_count:,} attached to enactments) in {t_elapsed:.2f}s!")


def export_results(results, G):
    """
    Exports summary report and edge lists.
    """
    print("[6/6] Serializing knowledge graph artifacts to disk...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    summary_file = os.path.join(OUTPUT_DIR, "statutory_kg_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Save compact edge manifest
    edge_types = Counter([d.get("relation") for u, v, d in G.edges(data=True)])
    print(f"      Knowledge graph serialized to '{summary_file}'!")
    print(f"      Final Topology Summary:")
    print(f"      - Total Vertices: {G.number_of_nodes():,}")
    print(f"      - Total Edges: {G.number_of_edges():,}")
    for rel, count in edge_types.most_common():
        print(f"        * {rel}: {count:,}")


def main():
    print("=" * 70)
    print("STATUTORY KNOWLEDGE GRAPH BUILDER & TOPOLOGICAL BENCHMARK ENGINE")
    print("Institution: Ateneo de Davao University, Department of Computer Science")
    print("=" * 70)
    t_global = time.time()

    # Step 1: Aliases & Metadata
    enactment_meta, alias_to_id = build_alias_registry()

    # Step 2: Edge Extraction
    edges_cites, edges_amends, edges_repeals = extract_edges(enactment_meta, alias_to_id)

    # Step 3: Graph Assembly
    G = assemble_graph(enactment_meta, edges_cites, edges_amends, edges_repeals)

    # Step 4: Topological Experiments
    results = run_topological_experiments(G, enactment_meta)

    # Step 5: Provision Linking
    link_provisions(G)

    # Step 6: Export Results
    export_results(results, G)

    total_time = time.time() - t_global
    print("=" * 70)
    print(f"SUCCESS: Statutory Knowledge Graph built and evaluated in {total_time:.2f}s!")
    print("=" * 70)


if __name__ == "__main__":
    main()

