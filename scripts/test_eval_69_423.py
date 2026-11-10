import sys
sys.path.insert(0, ".")
import time
import json
from pathlib import Path
from src.demo.app import NEURAL_ENGINE, chunk_ordinance_sections, resolve_statute_passage
from src.knowledge_graph.build_statutory_kg import build_alias_registry

print("=" * 80)
print("TESTING FULL UNABRIDGED AUDIT ON SECTION 69 & SECTION 423 OF ORDINANCE 0158-05")
print("=" * 80)

# Load full text of 0158-05
txt_path = Path("corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt")
raw_text = txt_path.read_text(encoding="utf-8")
doc_title, chunks = chunk_ordinance_sections(raw_text, default_title="Ordinance No. 0158-05")

sec_69 = next((c for c in chunks if str(c.get("sec_num")) == "69"), None)
sec_423 = next((c for c in chunks if str(c.get("sec_num")) == "423"), None)

test_sections = [
    ("Section 69 (ARC Investors Holding Tax)", sec_69, "Republic Act No. 7160 §143(f); Republic Act No. 8791 §3"),
    ("Section 423 (First Meridian Payment Under Protest)", sec_423, "Republic Act No. 7160 §195")
]

for label, sec, target_statute in test_sections:
    print(f"\n[*] Evaluating {label}...")
    if not sec:
        print("  Error: Section not found!")
        continue
        
    s_title = sec.get("sec_title", "")
    s_text = sec.get("text", "")
    query_str = f"[{doc_title} | SECTION {sec.get('sec_num')}: {s_title}] {s_text[:800]}"
    
    # 1. Unaugmented Stage 1 Retrieval
    t0 = time.time()
    raw_cands = NEURAL_ENGINE.retrieve_top_k(query_str, k=20, scope="national")
    retr_time = time.time() - t0
    print(f"  Stage 1 Retrieval ({retr_time:.2f}s): Top 5 candidates:")
    found_target = False
    for r_idx, c in enumerate(raw_cands[:5]):
        cit = c.get("citation", "")
        print(f"    {r_idx+1}. {cit} (sim: {c.get('similarity', 0.0):.4f})")
        if any(ts.split("§")[0].strip().lower() in cit.lower() for ts in target_statute.split(";")):
            found_target = True
            
    # 2. Stage 2 Cross-Encoder Scoring on Target Premise
    # Resolve target statute premise text
    t_title, stat_text = resolve_statute_passage(target_statute.split(";")[0].strip())
    premise_str = f"[{target_statute.split(';')[0].strip()}] {stat_text}"
    hypo_str = f"[SECTION {sec.get('sec_num')}: {s_title}] {s_text[:800]}"
    
    scores = NEURAL_ENGINE.evaluate_cross_encoder_batch([(premise_str, hypo_str)])[0]
    p_contra = scores["p_contradiction"]
    p_entail = scores["p_entailment"]
    p_neut = scores["p_neutral"]
    
    verdict = "CONTRADICTION" if p_contra >= 0.45 else ("ENTAILMENT" if p_entail >= 0.45 else "NEUTRAL")
    print(f"  Stage 2 DeBERTa-v3 Verdict against {target_statute.split(';')[0].strip()}:")
    print(f"    P(Contra): {p_contra*100:.2f}% | P(Entail): {p_entail*100:.2f}% | P(Neut): {p_neut*100:.2f}%")
    print(f"    Verdict: {verdict} (tau* = 0.45)")

