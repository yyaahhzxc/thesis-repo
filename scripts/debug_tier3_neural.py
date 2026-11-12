import sys
sys.path.insert(0, ".")
import json
from src.demo.app import NEURAL_ENGINE, resolve_statute_passage

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    cases = [json.loads(l) for l in f if l.strip()]

print(f"Loaded {len(cases)} cases.")
for c in cases:
    cid = c["case_id"]
    gold = c.get("gold_nli_label", "")
    primary_stat = c["controlling_statute"].split(";")[0].strip()
    premise_text = c.get("premise_text", "")
    hypo_text = c.get("challenged_text", "")
    ord_no = c.get("ordinance_no", "")
    
    t_title, stat_passage = resolve_statute_passage(primary_stat, premise_text)
    if not stat_passage or len(stat_passage.strip()) < 10:
        stat_passage = premise_text
    
    full_premise = f"[{primary_stat}] {stat_passage}"
    full_hypothesis = f"[{ord_no}] {hypo_text}"
    
    res = NEURAL_ENGINE.evaluate_cross_encoder_batch([(full_premise, full_hypothesis)])[0]
    pc = res["p_contradiction"] * 100
    pe = res["p_entailment"] * 100
    pn = res["p_neutral"] * 100
    print(f"{cid:<15} | Gold: {gold:<13} | P(C): {pc:5.1f}% | P(E): {pe:5.1f}% | P(N): {pn:5.1f}%")

