"""
generate_kg_visualization_data.py
=================================
Extracts a curated, multi-level Knowledge Graph payload for the interactive
Statutory Knowledge Graph Web Explorer:

1. Macro-Domain Hubs (8 domains)
2. National Statutory Super-Hubs (Top 30 by PageRank and citation count)
3. Davao City Local Enactments (Active ordinances + Top cited local laws)
4. Granular Statutory Sections (Tier 3 Supreme Court cases, conflicting pairs, and core sections)
5. Multi-Relational Edges:
   - CITES_AUTHORITY
   - AMENDS
   - REPEALS
   - GOVERNS_DOMAIN
   - CONTAINS (Enactment -> Section)
   - CONTRADICTION / ENTAILMENT (Tier 3 Ground-Truth Jurisprudence links)
"""

import json
import os
import re
from collections import Counter, defaultdict

CORPUS_NATIONAL = "corpus/cleaned/national/categorized_national_laws.jsonl"
CORPUS_LOCAL = "corpus/city_ordinances/categorized_davao_ordinances.jsonl"
UNIFIED_PROVISIONS = "data/unified_dual_statutory_provisions.jsonl"
SUMMARY_FILE = "output/knowledge_graph/statutory_kg_summary.json"
TIER3_FILE = "ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl"
OUTPUT_DIR = "output/knowledge_graph"
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "interactive_kg_data.json")

MACRO_DOMAINS = [
    {"id": "domain_0", "name": "General Administration, Organization & Civil Service", "color": "#4A90E2"},
    {"id": "domain_1", "name": "Public Finance, Taxation, Fiscal Policy & Budget", "color": "#F5A623"},
    {"id": "domain_2", "name": "Police Power, Public Order, Safety & Penal Law", "color": "#D0021B"},
    {"id": "domain_3", "name": "Social Services, Education, Labor & Human Development", "color": "#7ED321"},
    {"id": "domain_4", "name": "Public Works, Transportation, Utilities & Infrastructure", "color": "#9013FE"},
    {"id": "domain_5", "name": "Commerce, Trade, Industry, Agriculture & Economic Enterprise", "color": "#50E3C2"},
    {"id": "domain_6", "name": "Environmental Protection, Zoning, Land Use & Natural Resources", "color": "#417505"},
    {"id": "domain_7", "name": "Executive Issuances & Policy Reorganization", "color": "#B8E986"}
]

DOMAIN_NAME_TO_ID = {d["name"]: d["id"] for d in MACRO_DOMAINS}
DOMAIN_NAME_TO_COLOR = {d["name"]: d["color"] for d in MACRO_DOMAINS}

def main():
    print("[1/5] Loading summary topological metrics...")
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        kg_summary = json.load(f)

    super_hubs = kg_summary["experiment_1_super_hubs"]["top_overall_super_hubs"]
    davao_authorities = kg_summary["experiment_1_super_hubs"]["top_davao_authorities"]
    longest_lineage = kg_summary["experiment_5_lineage_dag"]["longest_amendatory_lineage"]

    selected_enactment_ids = set()
    for sh in super_hubs[:35]:
        selected_enactment_ids.add(sh["id"])
    for da in davao_authorities[:25]:
        selected_enactment_ids.add(da["id"])
    for ll in longest_lineage:
        selected_enactment_ids.add(ll["id"])

    # Load Tier 3 cases to make sure all Tier 3 ordinances and national statutes are included
    print("[2/5] Ingesting Tier 3 Supreme Court jurisprudence cases...")
    tier3_cases = []
    with open(TIER3_FILE, "r", encoding="utf-8") as f:
        for line in f:
            t3 = json.loads(line)
            tier3_cases.append(t3)

    # Build node and edge collections
    nodes = []
    edges = []
    added_node_ids = set()
    added_edge_keys = set()

    # 1. Add Domain Nodes
    for dom in MACRO_DOMAINS:
        nodes.append({
            "id": dom["id"],
            "label": dom["name"],
            "title": f"<b>Macro-Domain:</b> {dom['name']}",
            "group": "domain",
            "level": 0,
            "value": 40,
            "color": {
                "background": dom["color"],
                "border": "#FFFFFF",
                "highlight": {"background": "#FFFFFF", "border": dom["color"]}
            },
            "font": {"color": "#FFFFFF", "size": 14, "bold": True},
            "shape": "hexagon",
            "meta": {
                "type": "Domain Hub",
                "name": dom["name"]
            }
        })
        added_node_ids.add(dom["id"])

    # Ingest enactment metadata
    print("[3/5] Indexing enactment metadata and specific sections...")
    enactment_meta = {}
    from src.knowledge_graph.build_statutory_kg import build_alias_registry
    all_meta, alias_to_id = build_alias_registry()

    # Always include ordinances of Tier 3 cases
    tier3_ord_aliases = [
        ("ord", 309), ("ord", 92), ("ord", 158), ("ord", 325),
        ("ord", 367), ("ord", 270), ("ord", 3375), ("ord", 7783)
    ]
    for key in tier3_ord_aliases:
        if key in alias_to_id:
            selected_enactment_ids.add(alias_to_id[key])

    # Also pick top active Davao City ordinances across different domains
    local_count_by_domain = defaultdict(int)
    for eid, meta in all_meta.items():
        if meta.get("jurisdiction") == "local":
            dom = meta.get("domain", "")
            if local_count_by_domain[dom] < 12:
                selected_enactment_ids.add(eid)
                local_count_by_domain[dom] += 1

    print(f"      Selected {len(selected_enactment_ids)} enactments for visual graph.")

    # Hub in-degrees lookup
    hub_metrics = {sh["id"]: sh for sh in super_hubs}
    davao_cites_lookup = {da["id"]: da["davao_citations"] for da in davao_authorities}

    # Add Enactment Nodes
    for eid in selected_enactment_ids:
        if eid not in all_meta:
            continue
        meta = all_meta[eid]
        is_local = meta.get("jurisdiction") == "local"
        sh_info = hub_metrics.get(eid, {})
        in_deg = sh_info.get("in_degree", davao_cites_lookup.get(eid, 1))
        pr = sh_info.get("pagerank", 0.0005)
        dom = meta.get("domain", "General Administration, Organization & Civil Service")
        dom_color = DOMAIN_NAME_TO_COLOR.get(dom, "#4A90E2")

        # Determine visual properties
        if is_local:
            node_color = "#00D2D3"  # Vibrant Cyan/Teal for Local Ordinances
            border_color = "#01A3A4"
            group = "local_ordinance"
            shape = "box"
            val = min(35, max(14, 10 + in_deg * 2))
        else:
            node_color = "#FF9F43" if in_deg > 100 else "#FECA57"  # Warm Gold/Amber for National Statutes
            border_color = "#EE5253" if in_deg > 500 else "#F368E0"
            group = "national_statute"
            shape = "dot"
            val = min(50, max(15, int(15 + (in_deg ** 0.5) * 2.2)))

        num_label = meta.get("number", eid)
        if len(num_label) > 30:
            num_label = num_label[:28] + "..."

        nodes.append({
            "id": eid,
            "label": num_label,
            "title": f"<b>{meta.get('number')}</b><br><b>Jurisdiction:</b> {meta.get('jurisdiction').upper()}<br><b>Year:</b> {meta.get('year')}<br><b>Domain:</b> {dom}<br><b>In-Degree Centrality:</b> {in_deg}<br><b>PageRank:</b> {pr:.6f}<br><b>Title:</b> {meta.get('title')[:160]}...",
            "group": group,
            "level": 1 if not is_local else 2,
            "value": val,
            "color": {
                "background": node_color,
                "border": border_color,
                "highlight": {"background": "#FFFFFF", "border": border_color}
            },
            "font": {"color": "#FFFFFF", "size": 12},
            "shape": shape,
            "meta": {
                "id": eid,
                "number": meta.get("number"),
                "jurisdiction": meta.get("jurisdiction"),
                "year": meta.get("year"),
                "domain": dom,
                "in_degree": in_deg,
                "pagerank": pr,
                "title": meta.get("title")
            }
        })
        added_node_ids.add(eid)

        # Connect to domain hub
        dom_id = DOMAIN_NAME_TO_ID.get(dom)
        if dom_id and dom_id in added_node_ids:
            edges.append({
                "from": dom_id,
                "to": eid,
                "relation": "GOVERNS_DOMAIN",
                "arrows": "to",
                "color": {"color": "rgba(255,255,255,0.12)", "highlight": dom_color},
                "dashes": True,
                "width": 1
            })

    # 4. Add Granular Sections and Jurisprudential Conflict Links from Tier 3
    print("[4/5] Adding Tier 3 Granular Sections & Conflict/Entailment Edges...")
    for t3 in tier3_cases:
        cid = t3["case_id"]
        ord_no = t3.get("ordinance_no")
        statute_cit = t3.get("controlling_statute")
        gold_label = t3.get("gold_nli_label", "Contradiction")
        ruling = t3.get("ruling", "")
        chall_text = t3.get("challenged_text", "")
        prem_text = t3.get("premise_text", "")

        sec_node_id = f"sec_{cid.lower()}"
        stat_sec_id = f"stat_sec_{cid.lower()}"

        # Section Node (Challenged Ordinance Section)
        nodes.append({
            "id": sec_node_id,
            "label": f"§ {ord_no[:18]}",
            "title": f"<b>Challenged Provision: {ord_no}</b><br><b>Case:</b> {t3['case_name']}<br><b>Ruling:</b> {ruling}<br><b>Challenged Provision Text:</b><br>{chall_text[:250]}...",
            "group": "ordinance_section",
            "level": 3,
            "value": 16,
            "color": {
                "background": "#FF6B6B" if gold_label == "Contradiction" else "#1DD1A1",
                "border": "#EE5253" if gold_label == "Contradiction" else "#10AC84",
                "highlight": {"background": "#FFFFFF", "border": "#FF6B6B"}
            },
            "font": {"color": "#FFFFFF", "size": 11, "bold": True},
            "shape": "star" if gold_label == "Contradiction" else "diamond",
            "meta": {
                "case_id": cid,
                "case_name": t3["case_name"],
                "provision_text": chall_text,
                "ruling": ruling,
                "status": "Challenged Provision"
            }
        })
        added_node_ids.add(sec_node_id)

        # Statute Section Node (Controlling Premise Section)
        nodes.append({
            "id": stat_sec_id,
            "label": f"§ {statute_cit[:18]}",
            "title": f"<b>Controlling Statute Provision: {statute_cit}</b><br><b>Statute Title:</b> {t3.get('statute_title')}<br><b>Verbatim Text:</b><br>{prem_text[:250]}...",
            "group": "statute_section",
            "level": 2,
            "value": 16,
            "color": {
                "background": "#54A0FF",
                "border": "#2E86DE",
                "highlight": {"background": "#FFFFFF", "border": "#54A0FF"}
            },
            "font": {"color": "#FFFFFF", "size": 11},
            "shape": "triangle",
            "meta": {
                "case_id": cid,
                "statute_citation": statute_cit,
                "statute_title": t3.get("statute_title"),
                "premise_text": prem_text,
                "status": "Controlling Statutory Benchmark"
            }
        })
        added_node_ids.add(stat_sec_id)

        # Semantic NLI Conflict/Entailment Edge between the two sections!
        is_conflict = gold_label == "Contradiction"
        edges.append({
            "from": sec_node_id,
            "to": stat_sec_id,
            "relation": "CONTRADICTION" if is_conflict else "ENTAILMENT",
            "label": "CONFLICT (OVERTURNED)" if is_conflict else "VALID (UPHELD)",
            "arrows": "to;from",
            "color": {
                "color": "#FF4757" if is_conflict else "#2ED573",
                "highlight": "#FF4757" if is_conflict else "#2ED573"
            },
            "width": 3 if is_conflict else 2,
            "dashes": True if is_conflict else False,
            "font": {"color": "#FF4757" if is_conflict else "#2ED573", "size": 10, "strokeWidth": 2, "strokeColor": "#0F141C"}
        })

    # 5. Extract Authentic Citation and Amendatory Edges among selected enactments
    print("[5/5] Extracting citation and amendatory edges between nodes...")
    from src.knowledge_graph.build_statutory_kg import extract_edges
    cites, amends, repeals = extract_edges(all_meta, alias_to_id)

    # Citation Edges
    for (u, v), count in cites.items():
        if u in added_node_ids and v in added_node_ids:
            edges.append({
                "from": u,
                "to": v,
                "relation": "CITES_AUTHORITY",
                "arrows": "to",
                "title": f"Citations: {count}",
                "color": {"color": "rgba(100, 150, 255, 0.35)", "highlight": "#54A0FF"},
                "width": min(4, 1 + count // 3)
            })

    # Amendatory Edges
    for (u, v) in amends:
        if u in added_node_ids and v in added_node_ids:
            edges.append({
                "from": u,
                "to": v,
                "relation": "AMENDS",
                "arrows": "to",
                "label": "AMENDS",
                "color": {"color": "#FFA502", "highlight": "#FFA502"},
                "width": 2.5,
                "font": {"color": "#FFA502", "size": 9, "strokeWidth": 2, "strokeColor": "#0F141C"}
            })

    # Repealing Edges
    for (u, v) in repeals:
        if u in added_node_ids and v in added_node_ids:
            edges.append({
                "from": u,
                "to": v,
                "relation": "REPEALS",
                "arrows": "to",
                "label": "REPEALS",
                "color": {"color": "#FF6B81", "highlight": "#FF6B81"},
                "width": 2.5,
                "font": {"color": "#FF6B81", "size": 9, "strokeWidth": 2, "strokeColor": "#0F141C"}
            })

    # Link Tier 3 Section nodes to their parent enactments if present
    for t3 in tier3_cases:
        cid = t3["case_id"]
        sec_node_id = f"sec_{cid.lower()}"
        stat_sec_id = f"stat_sec_{cid.lower()}"
        
        # Link section to local enactment
        for nid in added_node_ids:
            if "0158_05" in nid or "158_05" in nid:
                if "158-05" in t3.get("ordinance_no", ""):
                    edges.append({
                        "from": nid, "to": sec_node_id,
                        "relation": "CONTAINS", "arrows": "to",
                        "color": {"color": "rgba(0, 210, 211, 0.45)"}, "width": 1.5
                    })
                    break
            elif "0270_23" in nid and "0270-23" in t3.get("ordinance_no", ""):
                edges.append({
                    "from": nid, "to": sec_node_id,
                    "relation": "CONTAINS", "arrows": "to",
                    "color": {"color": "rgba(0, 210, 211, 0.45)"}, "width": 1.5
                })
                break
            elif "0367_12" in nid and "0367-12" in t3.get("ordinance_no", ""):
                edges.append({
                    "from": nid, "to": sec_node_id,
                    "relation": "CONTAINS", "arrows": "to",
                    "color": {"color": "rgba(0, 210, 211, 0.45)"}, "width": 1.5
                })
                break

        # Link statute section to national super hub
        for nid in added_node_ids:
            if "ra_7160_1991" in nid and "7160" in t3.get("controlling_statute", ""):
                edges.append({
                    "from": nid, "to": stat_sec_id,
                    "relation": "CONTAINS", "arrows": "to",
                    "color": {"color": "rgba(255, 159, 67, 0.45)"}, "width": 1.5
                })
                break

    payload = {
        "summary": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "domains_count": len(MACRO_DOMAINS),
            "top_super_hubs": super_hubs[:10],
            "top_davao_authorities": davao_authorities[:10],
            "longest_lineage": longest_lineage
        },
        "nodes": nodes,
        "edges": edges,
        "tier3_cases": tier3_cases
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"SUCCESS: Interactive Graph payload written to '{OUTPUT_JSON}'!")
    print(f"  Nodes: {len(nodes)} (Domains: {len(MACRO_DOMAINS)}, Enactments: {len(nodes)-len(MACRO_DOMAINS)-20}, Provisions: 20)")
    print(f"  Edges: {len(edges)}")

if __name__ == "__main__":
    main()

