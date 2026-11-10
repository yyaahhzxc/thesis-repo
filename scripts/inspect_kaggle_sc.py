import json

with open('output/kaggle_cross_encoder_benchmark_results.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== Kaggle Cross-Encoder Benchmark Results (Table 4.24) ===")
for c in d.get('case_level_results', []):
    cid = c.get('case_id')
    gold = c.get('gold_label')
    pred = c.get('predicted_label')
    pc = c.get('p_contradiction')
    pe = c.get('p_entailment')
    print(f"[{cid}] Gold: {gold:<13} | Pred: {pred:<13} | P(Contra): {pc:.4f} | P(Entail): {pe:.4f}")

