import sys
sys.path.insert(0, ".")
import json
import time
from pathlib import Path
from src.demo.app import NEURAL_ENGINE, resolve_statute_passage

TIER3_BENCHMARK_PATH = Path("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl")

cases = []
with open(TIER3_BENCHMARK_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            cases.append(json.loads(line))

CASE_DOMAINS = {
    "DAVAO-TIER3-01": "Environmental Protection, Zoning, Land Use & Natural Resources",
    "DAVAO-TIER3-02": "Police Power, Public Order, Safety & Penal Law",
    "DAVAO-TIER3-03": "Public Finance, Taxation, Fiscal Policy & Budget",
    "DAVAO-TIER3-04": "Public Finance, Taxation, Fiscal Policy & Budget",
    "DAVAO-TIER3-05": "Public Finance, Taxation, Fiscal Policy & Budget",
    "DAVAO-TIER3-06": "Environmental Protection, Zoning, Land Use & Natural Resources",
    "DAVAO-TIER3-07": "Police Power, Public Order, Safety & Penal Law",
    "DAVAO-TIER3-08": "Public Works, Transportation, Utilities & Infrastructure",
    "SC-PHIL-09": "Police Power, Public Order, Safety & Penal Law",
    "SC-PHIL-10": "Police Power, Public Order, Safety & Penal Law",
}

baseline_pairs = []
domain_pairs = []
full_pairs = []

for c in cases:
    cid = c["case_id"]
    ord_no = c["ordinance_no"]
    hypo_text = c["challenged_text"]
    target_statute = c["controlling_statute"]
    premise_text = c["premise_text"]
    stat_title = c.get("statute_title", "")
    
    primary_stat = target_statute.split(";")[0].strip()
    t_title, stat_passage = resolve_statute_passage(primary_stat, premise_text)
    if not stat_passage or len(stat_passage.strip()) < 10:
        stat_passage = premise_text
        
    domain = CASE_DOMAINS.get(cid, "General Administration, Organization & Civil Service")
    
    # 1. Baseline Pair (Original training format)
    base_prem = f"[{stat_title} {primary_stat}] {stat_passage}"
    base_hypo = f"[{ord_no}] {hypo_text}"
    baseline_pairs.append((base_prem, base_hypo))
    
    # 2. Domain-Only Pair
    dom_prem = f"[{domain}] [{stat_title} {primary_stat}] {stat_passage}"
    dom_hypo = f"[{domain}] [{ord_no}] {hypo_text}"
    domain_pairs.append((dom_prem, dom_hypo))
    
    # 3. Full Metadata (with Jurisdiction)
    m1_prem = f"[JURISDICTION: NATIONAL | DOMAIN: {domain}] [{stat_title} {primary_stat}] {stat_passage}"
    m1_hypo = f"[JURISDICTION: LOCAL | DOMAIN: {domain}] [{ord_no}] {hypo_text}"
    full_pairs.append((m1_prem, m1_hypo))

res_base = NEURAL_ENGINE.evaluate_cross_encoder_batch(baseline_pairs)
res_dom = NEURAL_ENGINE.evaluate_cross_encoder_batch(domain_pairs)
res_full = NEURAL_ENGINE.evaluate_cross_encoder_batch(full_pairs)

print("\n" + "="*95)
print(f"{'Case ID':<15} | {'Gold':<13} | {'Baseline':<12} | {'Domain-Only':<14} | {'Full Meta (Jur)':<16}")
print("="*95)

for i, c in enumerate(cases):
    cid = c["case_id"]
    gold = c["gold_nli_label"]
    p_b = float(res_base[i]["p_contradiction"]) * 100
    p_d = float(res_dom[i]["p_contradiction"]) * 100
    p_f = float(res_full[i]["p_contradiction"]) * 100
    print(f"{cid:<15} | {gold:<13} | {p_b:>10.2f}% | {p_d:>12.2f}% | {p_f:>14.2f}%")
