import sys
sys.path.insert(0, ".")
import pypdf
from pathlib import Path
from src.demo.app import execute_full_ordinance_audit, NEURAL_ENGINE

pdf_path = Path("src/demo/sample_cases/pdf/09_magtajas_casino_preemption.pdf")
reader = pypdf.PdfReader(str(pdf_path))
raw_text = "\n".join(page.extract_text() for page in reader.pages)

print(f"Auditing complete document: {pdf_path.name} ({len(raw_text)} chars)...")
result = execute_full_ordinance_audit(raw_text, filename=pdf_path.name)

print("\n" + "=" * 60)
print(f"DOCUMENT AUDIT RESULT: {result['document_name']}")
print("=" * 60)
print(f"Total Sections Audited: {result['total_sections']}")
print(f"Triage Verdict:         {result['triage_verdict']}")
print(f"Document Flagged:       {result['is_flagged']}")
print(f"Contradictions Caught:  {result['counts']['contradiction']}")
print(f"Entailments / Clear:    {result['counts']['entailment']}")
print(f"Neutral Provisions:     {result['counts']['neutral']}")
print(f"Latency:                {result.get('latency_metrics', {}).get('total_latency_s', 'N/A')} s")
print("-" * 60)

for sec in result.get("sections", []):
    snum = sec.get("sec_num")
    stitle = sec.get("sec_title")
    verdict = sec.get("verdict_type")
    alert = sec.get("alert_level")
    print(f"\n[*] Section {snum}: {stitle} | Verdict: {verdict} ({alert})")
    print(f"    Text: {sec.get('text', '')[:100]}...")
    
    # Check top candidate
    cands = sec.get("candidates", [])
    if cands:
        top_cand = cands[0]
        print(f"    Top Statute: {top_cand.get('citation')}")
        print(f"    Statute Title: {top_cand.get('title')}")
        print(f"    P(Contradiction): {top_cand.get('p_contradiction', 0)*100:.2f}%")
        print(f"    P(Entailment):    {top_cand.get('p_entailment', 0)*100:.2f}%")
