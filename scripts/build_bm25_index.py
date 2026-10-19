import os
import sys
import json
import time
import pickle
import re
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dual_retrieval import tokenize_legal_text
from rank_bm25 import BM25Okapi

master_path = Path("data/unified_dual_statutory_provisions.jsonl")
output_path = Path("output/dual_corpus_bm25.pkl")

print(f"[BuildBM25] Reading {master_path}...")
t0 = time.time()

tokenized_corpus = []
doc_metadata = [] # stores (provision_id, enactment_number, is_primary)

with open(master_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if not line.strip():
            continue
        item = json.loads(line)
        pid = item.get("provision_id")
        enact = item.get("enactment_number", "")
        is_primary = "republic act" in enact.lower() or "batas pambansa" in enact.lower()
        doc_metadata.append((pid, enact, is_primary))
        
        # Tokenize prepended text + enactment title for BM25
        text_to_index = f"{enact} {item.get('enactment_title', '')} {item.get('section_number', '')} {item.get('section_title', '')} {item.get('prepended_text') or item.get('raw_text', '')}"
        tokens = tokenize_legal_text(text_to_index)
        tokenized_corpus.append(tokens)

t1 = time.time()
print(f"[BuildBM25] Read and tokenized {len(tokenized_corpus):,} provisions in {t1 - t0:.2f}s.")

print("[BuildBM25] Building BM25Okapi index...")
bm25 = BM25Okapi(tokenized_corpus)
t2 = time.time()
print(f"[BuildBM25] BM25Okapi constructed in {t2 - t1:.2f}s.")

print(f"[BuildBM25] Saving to {output_path}...")
with open(output_path, "wb") as f:
    pickle.dump({"bm25": bm25, "metadata": doc_metadata}, f, protocol=pickle.HIGHEST_PROTOCOL)
t3 = time.time()
print(f"[BuildBM25] Saved {output_path.stat().st_size / (1024*1024):.2f} MB in {t3 - t2:.2f}s! Total time: {t3 - t0:.2f}s.")
