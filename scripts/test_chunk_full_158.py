import sys
sys.path.insert(0, ".")
import time
import pypdf
from pathlib import Path
from src.demo.app import chunk_ordinance_sections

pdf_path = Path("ground_truth/tier3_sc_cases/tier3_landmark_ordinances_pdf/03_davao_revenue_code_2005_full.pdf")

t0 = time.time()
reader = pypdf.PdfReader(str(pdf_path))
pages_text = [page.extract_text() or "" for page in reader.pages]
full_text = "\n\n".join(pages_text)
extract_time = time.time() - t0
print(f"Extracted {len(reader.pages)} pages ({len(full_text.split()):,} words) in {extract_time:.2f}s.")

t1 = time.time()
doc_title, chunks = chunk_ordinance_sections(full_text, default_title="Ordinance No. 0158-05")
chunk_time = time.time() - t1
print(f"Parsed {len(chunks)} sections in {chunk_time:.2f}s.")

substantive = [c for c in chunks if not c.get("is_boilerplate", False)]
boilerplate = [c for c in chunks if c.get("is_boilerplate", False)]
print(f"Substantive sections: {len(substantive)} | Boilerplate: {len(boilerplate)}")

# Check target sections
sec_69 = next((c for c in chunks if str(c.get("sec_num")) == "69"), None)
sec_423 = next((c for c in chunks if str(c.get("sec_num")) == "423"), None)

if sec_69:
    print(f"\n[FOUND] Section 69: {sec_69.get('sec_title')} (words: {len(sec_69['text'].split())})")
    print("  Snippet:", sec_69['text'][:150])
else:
    print("\n[MISSING] Section 69 not found in chunks!")

if sec_423:
    print(f"\n[FOUND] Section 423: {sec_423.get('sec_title')} (words: {len(sec_423['text'].split())})")
    print("  Snippet:", sec_423['text'][:150])
else:
    print("\n[MISSING] Section 423 not found in chunks!")
