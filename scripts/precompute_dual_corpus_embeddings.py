"""
precompute_dual_corpus_embeddings.py
====================================
Offline Pre-computation of Dense Vector Representations for the Unified Dual Statutory Corpus.

Encodes all 176,421 provisions (164,620 national + 11,801 municipal) using the
production workhorse Bi-Encoder (sentence-transformers/all-MiniLM-L6-v2, 384 dims)
with context-prepended structural headers.

Robust Design:
- Memory-mapped direct-to-disk writing (np.memmap) with flat <500 MB RAM footprint
- Resumable: Detects existing progress and resumes automatically without loss
- Real-time audit log in output/embedding_progress.json
- Optimized max_seq_length=256 (matches empirical Stage 1 screening context)
- Generates output/dual_corpus_embeddings_minilm.npy (shape: 176421, 384, float32, 271 MB)
- Generates output/dual_corpus_embeddings_meta.json (Manifest and provision ID index)

Usage:
  python scripts/precompute_dual_corpus_embeddings.py
  python scripts/precompute_dual_corpus_embeddings.py --batch-size 256 --resume
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

INPUT_DATA_FILE = Path("data/unified_dual_statutory_provisions.jsonl")
OUTPUT_EMB_FILE = Path("output/dual_corpus_embeddings_minilm.npy")
OUTPUT_META_FILE = Path("output/dual_corpus_embeddings_meta.json")
PROGRESS_FILE = Path("output/embedding_progress.json")

TOTAL_CORPUS_SIZE = 176421
EMBEDDING_DIM = 384


def parse_args():
    parser = argparse.ArgumentParser(description="Precompute dense vectors for unified corpus.")
    parser.add_argument("--batch-size", type=int, default=256, help="Encoding batch size (default: 256)")
    parser.add_argument("--threads", type=int, default=4, help="PyTorch CPU thread count (default: 4)")
    parser.add_argument("--max-seq-len", type=int, default=256, help="Transformer attention sequence length (default: 256)")
    parser.add_argument("--reset", action="store_true", help="Force restart from index 0 instead of resuming")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for testing")
    return parser.parse_args()


def run_precomputation():
    args = parse_args()
    torch.set_num_threads(args.threads)

    print("=" * 80)
    print("STAGE 1: RESUMABLE OFFLINE DENSE EMBEDDING PRE-COMPUTATION")
    print("=" * 80)
    print(f"Master Corpus:      {INPUT_DATA_FILE}")
    print(f"Bi-Encoder Model:   sentence-transformers/all-MiniLM-L6-v2 ({EMBEDDING_DIM} dims)")
    print(f"Batch Size:         {args.batch_size}")
    print(f"Max Sequence Len:   {args.max_seq_len} tokens")
    print(f"Target Output:      {OUTPUT_EMB_FILE} ({TOTAL_CORPUS_SIZE * EMBEDDING_DIM * 4 / (1024*1024):.2f} MB)")

    if not INPUT_DATA_FILE.exists():
        raise FileNotFoundError(f"Missing master provisions: {INPUT_DATA_FILE}. Run scripts/build_unified_dual_corpus_provisions.py first.")

    # 1. Read provision metadata and text lines
    t0 = time.time()
    print("\n[1/3] Ingesting provision IDs and prepended texts...")
    provision_ids = []
    prepended_texts = []
    jurisdictions = []
    operative_flags = []

    with open(INPUT_DATA_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            provision_ids.append(item['provision_id'])
            prepended_texts.append(item['prepended_text'])
            jurisdictions.append(item['jurisdiction'])
            operative_flags.append(item['is_operative'])
            
            if args.limit and len(provision_ids) >= args.limit:
                break

    n_total = len(provision_ids)
    t1 = time.time()
    print(f"Loaded {n_total:,} provisions in {t1 - t0:.2f}s.")

    # 2. Check resume status
    start_idx = 0
    if OUTPUT_EMB_FILE.exists() and not args.reset:
        try:
            # Check if file has target size
            expected_bytes = 128 + (n_total * EMBEDDING_DIM * 4) # npy header + data
            actual_bytes = OUTPUT_EMB_FILE.stat().st_size
            if actual_bytes == expected_bytes and PROGRESS_FILE.exists():
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as pf:
                    prog_info = json.load(pf)
                    start_idx = prog_info.get("completed_provisions", 0)
                    if start_idx >= n_total:
                        print(f"[Resume] Embeddings already complete ({start_idx:,}/{n_total:,}). Exiting.")
                        return
                    print(f"[Resume] Resuming from provision index {start_idx:,} ({start_idx/n_total*100:.1f}% complete)...")
        except Exception as e:
            print(f"[Resume Warning] Could not verify existing file: {e}. Starting fresh.")
            start_idx = 0

    # 3. Create or open memory-mapped array directly on disk
    if start_idx == 0:
        # Pre-allocate zero array and save header
        print(f"Allocating memory-mapped array for {n_total:,} vectors on disk...")
        init_arr = np.zeros((n_total, EMBEDDING_DIM), dtype=np.float32)
        np.save(OUTPUT_EMB_FILE, init_arr)
        del init_arr

    # Open with read/write memory mapping
    emb_memmap = np.load(OUTPUT_EMB_FILE, mmap_mode='r+')

    # 4. Initialize Model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n[2/3] Loading SentenceTransformer all-MiniLM-L6-v2 on {device.upper()}...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=device)
    model.max_seq_length = args.max_seq_len
    t2 = time.time()
    print(f"Model ready in {t2 - t1:.2f}s. Max sequence length set to {model.max_seq_length}.")

    # 5. Batch Encoding Loop
    print(f"\n[3/3] Encoding provisions from index {start_idx:,} to {n_total:,} in batches of {args.batch_size}...")
    batch_size = args.batch_size
    t_start_loop = time.time()
    last_log_time = t_start_loop
    items_done_session = 0

    for curr_idx in range(start_idx, n_total, batch_size):
        end_idx = min(curr_idx + batch_size, n_total)
        batch = prepended_texts[curr_idx:end_idx]

        # Normalized embeddings so dot-product equals cosine similarity
        batch_embs = model.encode(
            batch,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True
        )

        emb_memmap[curr_idx:end_idx] = batch_embs.astype(np.float32)
        items_done_session += len(batch)

        curr_time = time.time()
        # Save progress and log every 10 seconds or at completion
        if end_idx == n_total or (curr_time - last_log_time) >= 10.0 or (end_idx % 5000 < batch_size):
            emb_memmap.flush()
            elapsed_session = curr_time - t_start_loop
            rate = items_done_session / max(elapsed_session, 0.001)
            remaining_items = n_total - end_idx
            eta_mins = (remaining_items / max(rate, 0.001)) / 60.0
            pct = (end_idx / n_total) * 100

            progress_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_provisions": n_total,
                "completed_provisions": end_idx,
                "percent_complete": round(pct, 2),
                "throughput_prov_per_sec": round(rate, 2),
                "eta_minutes": round(eta_mins, 2),
                "elapsed_session_seconds": round(elapsed_session, 2)
            }
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as pf:
                json.dump(progress_dict, pf, indent=2)

            print(
                f"  [{pct:5.1f}%] Encoded {end_idx:,}/{n_total:,} | "
                f"Rate: {rate:5.1f} prov/s | ETA: {eta_mins:4.1f} min",
                flush=True
            )
            last_log_time = curr_time

    # Final flush to ensure all bytes are synced to disk
    emb_memmap.flush()
    t_end = time.time()
    total_time = t_end - t_start_loop
    print("\n" + "=" * 80)
    print("DENSE VECTOR PRE-COMPUTATION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print(f"Total Provisions Encoded: {n_total:,}")
    print(f"Total Time:               {total_time:.2f}s ({total_time/60.0:.2f} min)")
    print(f"Overall Throughput:       {items_done_session / max(total_time, 0.001):.1f} prov/s")
    print(f"Embeddings Array File:    {OUTPUT_EMB_FILE} ({OUTPUT_EMB_FILE.stat().st_size / (1024*1024):.2f} MB)")

    # Save manifest
    meta_manifest = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_id": "sentence-transformers/all-MiniLM-L6-v2",
        "dim": EMBEDDING_DIM,
        "dtype": "float32",
        "normalized": True,
        "total_provisions": n_total,
        "national_count": sum(1 for j in jurisdictions if j == 'national'),
        "municipal_count": sum(1 for j in jurisdictions if j == 'municipal'),
        "operative_count": sum(1 for op in operative_flags if op),
        "embeddings_file": str(OUTPUT_EMB_FILE),
        "provision_ids": provision_ids
    }
    with open(OUTPUT_META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta_manifest, f, indent=2, ensure_ascii=False)
    print(f"Manifest & ID Index:      {OUTPUT_META_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    run_precomputation()
