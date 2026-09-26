"""
dual_retrieval.py
=================
Dual-Stream Stage 1 Retrieval Engine for Ex-Ante Davao City Ordinances.

Combines Sparse Lexical Search (BM25Okapi) with Offline-Precomputed Dense Semantic
Embeddings (sentence-transformers/all-MiniLM-L6-v2) across the Unified 176,421-Provision
Statutory Corpus.

Architecture:
1. Dual Statutory Search Space:
   - National Corpus: 164,620 sections across 25,432 national statutes
   - Municipal Corpus: 11,801 sections across 1,664 Davao City local ordinances
   - Total Space: 176,421 searchable provisions (172,780 operative substantive rules)
2. Dual-Stream Candidate Partitioning:
   - Stream A (Vertical Preemption): Superior national laws tested under Magtajas v. Pryce
   - Stream B (Horizontal Coherence): Fellow Davao City enactments tested for local consistency
3. Hybrid Fusion: Reciprocal Rank Fusion (RRF k=60) combining lexical and neural ranks.
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    raise ImportError("rank-bm25 is required. Run: pip install rank-bm25")

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

COMMON_LEGAL_STOPWORDS = {
    'the', 'of', 'and', 'in', 'to', 'a', 'is', 'that', 'this', 'be', 'for', 'with',
    'as', 'by', 'on', 'at', 'from', 'or', 'an', 'all', 'which', 'shall', 'any',
    'such', 'hereto', 'hereby', 'thereof', 'wherein', 'pursuant'
}


def tokenize_legal_text(text: str, remove_stopwords: bool = False) -> List[str]:
    """Lightweight legal tokenizer retaining alphanumeric tokens and legal symbols."""
    tokens = re.findall(r'[a-zA-Z0-9]+', text.lower())
    if remove_stopwords:
        tokens = [t for t in tokens if t not in COMMON_LEGAL_STOPWORDS]
    return tokens


class DualStreamRetrievalEngine:
    """
    Unified Stage 1 Dual-Stream Retrieval Engine over 176,421 Philippine statutory provisions.
    """
    def __init__(
        self,
        master_corpus_path: str = "data/unified_dual_statutory_provisions.jsonl",
        embeddings_path: str = "output/dual_corpus_embeddings_minilm.npy",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        mmap_embeddings: bool = True,
        load_dense: bool = True
    ):
        self.master_corpus_path = Path(master_corpus_path)
        self.embeddings_path = Path(embeddings_path)
        self.model_name = model_name
        self.mmap_embeddings = mmap_embeddings
        self.load_dense = load_dense

        # In-memory provision store
        self.provisions: List[Dict[str, Any]] = []
        self.provision_ids: List[str] = []
        self.id_to_idx: Dict[str, int] = {}
        
        # Stream partition masks
        self.national_indices: np.ndarray = np.array([], dtype=int)
        self.municipal_indices: np.ndarray = np.array([], dtype=int)
        self.operative_indices: np.ndarray = np.array([], dtype=int)

        # Lexical BM25 Engine
        self.bm25: Optional[BM25Okapi] = None
        self.tokenized_corpus: List[List[str]] = []

        # Dense Semantic Engine
        self.bi_encoder: Optional[Any] = None
        self.embeddings: Optional[np.ndarray] = None

        self._initialize_corpus()

    def _initialize_corpus(self):
        """Loads master provisions and builds the sparse BM25 inverted index."""
        t0 = time.time()
        print(f"[DualRetrieval] Loading master provisions from {self.master_corpus_path}...", flush=True)

        if not self.master_corpus_path.exists():
            raise FileNotFoundError(
                f"Master corpus not found at {self.master_corpus_path}. "
                f"Run 'python scripts/build_unified_dual_corpus_provisions.py' first."
            )

        nat_idx = []
        mun_idx = []
        op_idx = []

        with open(self.master_corpus_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if not line.strip():
                    continue
                p = json.loads(line)
                pid = p['provision_id']
                self.provisions.append(p)
                self.provision_ids.append(pid)
                self.id_to_idx[pid] = idx

                if p['jurisdiction'] == 'national':
                    nat_idx.append(idx)
                else:
                    mun_idx.append(idx)

                if p.get('is_operative', True):
                    op_idx.append(idx)

                # Tokenize prepended text for BM25
                tokens = tokenize_legal_text(p.get('prepended_text', ''))
                self.tokenized_corpus.append(tokens)

        self.national_indices = np.array(nat_idx, dtype=int)
        self.municipal_indices = np.array(mun_idx, dtype=int)
        self.operative_indices = np.array(op_idx, dtype=int)

        n_total = len(self.provisions)
        t1 = time.time()
        print(
            f"[DualRetrieval] Ingested {n_total:,} provisions in {t1 - t0:.2f}s "
            f"(National: {len(self.national_indices):,}, Municipal: {len(self.municipal_indices):,}, "
            f"Operative: {len(self.operative_indices):,}).",
            flush=True
        )

        print("[DualRetrieval] Constructing BM25Okapi inverted index over 176,421 provisions...", flush=True)
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        t2 = time.time()
        print(f"[DualRetrieval] BM25 inverted index constructed in {t2 - t1:.2f}s.", flush=True)

        # Initialize Dense Semantic Embeddings if available
        if self.load_dense:
            self._load_dense_embeddings()

    def _load_dense_embeddings(self):
        """Loads offline precomputed dense embeddings and initializes Bi-Encoder for query encoding."""
        if not self.embeddings_path.exists():
            print(
                f"[DualRetrieval] Notice: Precomputed embeddings not found at {self.embeddings_path}. "
                f"Operating in BM25-lexical mode. (Run 'python scripts/precompute_dual_corpus_embeddings.py' "
                f"to generate the offline .npy vector table).",
                flush=True
            )
            return

        t0 = time.time()
        print(f"[DualRetrieval] Loading precomputed dense embeddings from {self.embeddings_path}...", flush=True)
        if self.mmap_embeddings:
            self.embeddings = np.load(self.embeddings_path, mmap_mode='r')
            print(f"[DualRetrieval] Memory-mapped {self.embeddings.shape} embeddings ({self.embeddings.dtype}) with zero RAM bloat.", flush=True)
        else:
            self.embeddings = np.load(self.embeddings_path)
            print(f"[DualRetrieval] Loaded {self.embeddings.shape} embeddings into memory.", flush=True)

        t1 = time.time()
        print(f"[DualRetrieval] Dense embeddings loaded in {t1 - t0:.2f}s.", flush=True)

        # Initialize Bi-Encoder for query encoding (1.33 ms CPU latency)
        if SentenceTransformer:
            print(f"[DualRetrieval] Initializing query encoder: {self.model_name}...", flush=True)
            self.bi_encoder = SentenceTransformer(self.model_name, device='cpu')
            print("[DualRetrieval] Bi-Encoder query encoder initialized.", flush=True)

    def retrieve(
        self,
        query_text: str,
        k_vertical: int = 15,
        k_horizontal: int = 15,
        operative_only: bool = True,
        rrf_k: int = 60
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Executes dual-stream hybrid retrieval for an ex-ante local ordinance provision.
        
        Returns:
            {
                "vertical_national_candidates": [Top-k national statutory provisions],
                "horizontal_municipal_candidates": [Top-k fellow Davao City ordinances],
                "retrieval_metrics": {latency_ms, bm25_time_ms, dense_time_ms, ...}
            }
        """
        t_start = time.time()
        query_tokens = tokenize_legal_text(query_text)
        n_total = len(self.provisions)

        # 1. Sparse Lexical BM25 Scoring
        t_bm25_0 = time.time()
        bm25_scores = np.array(self.bm25.get_scores(query_tokens))
        t_bm25_1 = time.time()
        bm25_latency_ms = (t_bm25_1 - t_bm25_0) * 1000

        # 2. Dense Semantic Scoring
        dense_scores = None
        dense_latency_ms = 0.0
        if self.embeddings is not None and self.bi_encoder is not None:
            t_dense_0 = time.time()
            query_vec = self.bi_encoder.encode([query_text], normalize_embeddings=True)[0]
            # Inner dot-product on normalized vectors
            dense_scores = np.dot(self.embeddings, query_vec)
            t_dense_1 = time.time()
            dense_latency_ms = (t_dense_1 - t_dense_0) * 1000

        # 3. Reciprocal Rank Fusion (RRF k=60)
        t_fuse_0 = time.time()
        # BM25 Ranks (1-indexed)
        bm25_order = np.argsort(-bm25_scores)
        bm25_ranks = np.empty(n_total, dtype=int)
        bm25_ranks[bm25_order] = np.arange(1, n_total + 1)

        if dense_scores is not None:
            dense_order = np.argsort(-dense_scores)
            dense_ranks = np.empty(n_total, dtype=int)
            dense_ranks[dense_order] = np.arange(1, n_total + 1)

            rrf_scores = (1.0 / (rrf_k + bm25_ranks)) + (1.0 / (rrf_k + dense_ranks))
        else:
            rrf_scores = 1.0 / (rrf_k + bm25_ranks)

        t_fuse_1 = time.time()
        fusion_latency_ms = (t_fuse_1 - t_fuse_0) * 1000

        # 4. Stream Partitioning & Candidate Shortlisting
        def extract_top_candidates(target_indices: np.ndarray, top_k: int, norm_label: str) -> List[Dict[str, Any]]:
            if operative_only:
                # Mask out procedural boilerplate
                op_mask = np.isin(target_indices, self.operative_indices)
                valid_indices = target_indices[op_mask]
            else:
                valid_indices = target_indices

            sub_scores = rrf_scores[valid_indices]
            top_sub_order = np.argsort(-sub_scores)[:top_k]
            top_global_indices = valid_indices[top_sub_order]

            results = []
            for rank_idx, g_idx in enumerate(top_global_indices, 1):
                p = self.provisions[g_idx]
                results.append({
                    "rank": rank_idx,
                    "rrf_score": float(rrf_scores[g_idx]),
                    "bm25_score": float(bm25_scores[g_idx]),
                    "bm25_rank": int(bm25_ranks[g_idx]),
                    "dense_score": float(dense_scores[g_idx]) if dense_scores is not None else 0.0,
                    "dense_rank": int(dense_ranks[g_idx]) if dense_scores is not None else 0,
                    "provision_id": p['provision_id'],
                    "jurisdiction": p['jurisdiction'],
                    "enactment_number": p['enactment_number'],
                    "enactment_title": p['enactment_title'],
                    "year": p.get('year'),
                    "section_number": p['section_number'],
                    "section_title": p.get('section_title', ''),
                    "prepended_text": p['prepended_text'],
                    "raw_text": p['raw_text'],
                    "macro_domain": p.get('macro_domain', ''),
                    "normative_scope": norm_label
                })
            return results

        vertical_candidates = extract_top_candidates(
            self.national_indices,
            k_vertical,
            "Vertical Preemption (National Statute / Magtajas Doctrine)"
        )
        horizontal_candidates = extract_top_candidates(
            self.municipal_indices,
            k_horizontal,
            "Horizontal Coherence (Fellow Davao City Ordinance)"
        )

        t_end = time.time()
        total_latency_ms = (t_end - t_start) * 1000

        return {
            "query": query_text,
            "vertical_national_candidates": vertical_candidates,
            "horizontal_municipal_candidates": horizontal_candidates,
            "metrics": {
                "total_latency_ms": round(total_latency_ms, 2),
                "bm25_latency_ms": round(bm25_latency_ms, 2),
                "dense_latency_ms": round(dense_latency_ms, 2),
                "fusion_latency_ms": round(fusion_latency_ms, 2),
                "provisions_searched": n_total,
                "dense_enabled": dense_scores is not None
            }
        }


if __name__ == "__main__":
    print("Testing Dual-Stream Retrieval Engine on sample query...")
    engine = DualStreamRetrievalEngine()
    test_query = "Penalize drivers operating public utility tricycles on national highways exceeding 30 km/h"
    res = engine.retrieve(test_query, k_vertical=3, k_horizontal=3)
    
    print(f"\nQuery: {res['query']}")
    print(f"Total Search Latency: {res['metrics']['total_latency_ms']} ms (Dense: {res['metrics']['dense_latency_ms']} ms, BM25: {res['metrics']['bm25_latency_ms']} ms)")
    
    print("\n--- Top Vertical Preemption Candidates (National) ---")
    for c in res['vertical_national_candidates']:
        print(f"[{c['rank']}] RRF: {c['rrf_score']:.4f} | {c['enactment_number']} - {c['section_number']}: {c['section_title']}")
        print(f"    {c['raw_text'][:120]}...\n")

    print("--- Top Horizontal Coherence Candidates (Municipal) ---")
    for c in res['horizontal_municipal_candidates']:
        print(f"[{c['rank']}] RRF: {c['rrf_score']:.4f} | {c['enactment_number']} - {c['section_number']}: {c['section_title']}")
        print(f"    {c['raw_text'][:120]}...\n")
