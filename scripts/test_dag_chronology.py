import sys
sys.path.append('.')
import json
import networkx as nx
from src.knowledge_graph.build_statutory_kg import build_alias_registry
import re

enactment_meta, alias_to_id = build_alias_registry()

patterns = [
    ("ra", re.compile(r'(?:Republic\s+Act|R\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("pd", re.compile(r'(?:Presidential\s+Decree|P\.?\s*D\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("bp", re.compile(r'(?:Batas\s+Pambansa|B\.?\s*P\.?)\s*(?:Blg\.?\s*)?(\d+)', re.IGNORECASE)),
    ("ca", re.compile(r'(?:Commonwealth\s+Act|C\.?\s*A\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("eo", re.compile(r'(?:Executive\s+Order|E\.?\s*O\.?)\s*(?:No\.?\s*)?(\d+)', re.IGNORECASE)),
    ("act", re.compile(r'\bAct\s+No\.?\s*(\d+)', re.IGNORECASE)),
    ("ord", re.compile(r'(?:City\s+Ordinance|Ordinance)\s+No\.?\s*([0-9]+(?:-[0-9]+)?)', re.IGNORECASE)),
]

def find_targets(text_segment):
    found = set()
    for prefix, pat in patterns:
        for m in pat.finditer(text_segment):
            raw = m.group(1).lower()
            key = (prefix, int(raw) if prefix != "ord" else raw)
            tid = alias_to_id.get(key)
            if tid:
                found.add(tid)
    return found

amend_forward = re.compile(r'\b(?:hereby\s+amended|is\s+amended|are\s+amended|amending)\b', re.IGNORECASE)
amend_reverse = re.compile(r'\b(?:as\s+amended\s+by)\b', re.IGNORECASE)
repeal_forward = re.compile(r'\b(?:hereby\s+repealed|is\s+repealed|are\s+repealed|repealing)\b', re.IGNORECASE)

G_amend = nx.DiGraph()

for corpus_file in ["corpus/city_ordinances/categorized_davao_ordinances.jsonl", "corpus/categorized_national_laws.jsonl"]:
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            src_id = data.get("ordinance_id") or data.get("law_id")
            text = data.get("full_text", "")
            src_year = enactment_meta[src_id].get("year") or 9999

            # 1. Forward amends: src_id AMENDS target (src modifies target)
            for m in amend_forward.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta[tid].get("year") or 0
                        # Under lex posterior, amender must be >= target
                        if src_year >= tgt_year:
                            G_amend.add_edge(src_id, tid, rel="AMENDS")

            # 2. Reverse amends: "as amended by target" -> target AMENDS src_id
            for m in amend_reverse.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta[tid].get("year") or 0
                        if tgt_year >= src_year:
                            G_amend.add_edge(tid, src_id, rel="AMENDS")

            # 3. Repeals: src_id REPEALS target
            for m in repeal_forward.finditer(text):
                w = text[max(0, m.start() - 150) : min(len(text), m.end() + 150)]
                for tid in find_targets(w):
                    if tid != src_id:
                        tgt_year = enactment_meta[tid].get("year") or 0
                        if src_year >= tgt_year:
                            G_amend.add_edge(src_id, tid, rel="REPEALS")

print(f"Total amendatory nodes: {G_amend.number_of_nodes()}")
print(f"Total amendatory edges: {G_amend.number_of_edges()}")

is_dag = nx.is_directed_acyclic_graph(G_amend)
print(f"Is Strictly Acyclic DAG: {is_dag}")
if not is_dag:
    cycles = list(nx.simple_cycles(G_amend))
    print(f"Detected cycles: {len(cycles)}")
else:
    depth = nx.dag_longest_path_length(G_amend)
    path = nx.dag_longest_path(G_amend)
    print(f"Maximum Amendatory Depth: {depth}")
    print("Longest Amendatory Lineage Path:")
    for n in path:
        m = enactment_meta.get(n, {})
        print(f"  -> {m.get('number', n)} ({m.get('jurisdiction')}, {m.get('year')}): {m.get('title', '')[:60]}")

