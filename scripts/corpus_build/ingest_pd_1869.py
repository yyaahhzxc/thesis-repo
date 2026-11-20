"""Idempotent ingestion of Presidential Decree No. 1869 (PAGCOR Charter) into the unified corpus,
MiniLM dense embeddings, BM25 sparse index, and statutory Knowledge Graph.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

REPO_ROOT = Path(__file__).resolve().parents[2]
VERBATIM_PATH = REPO_ROOT / "data" / "corpus" / "national_statutes_supplements" / "pd_1869_1983_verbatim.txt"
UNIFIED_PATH = REPO_ROOT / "data" / "unified_dual_statutory_provisions.jsonl"
EMB_PATH = REPO_ROOT / "output" / "dual_corpus_embeddings_minilm.npy"
META_PATH = REPO_ROOT / "output" / "dual_corpus_embeddings_meta.json"
BM25_CSR_PATH = REPO_ROOT / "output" / "dual_corpus_bm25_fast.npz"
BM25_VOCAB_PATH = REPO_ROOT / "output" / "dual_corpus_bm25_vocab.json"
BM25_BUILD_SCRIPT = REPO_ROOT / "scripts" / "corpus_build" / "build_bm25_index.py"
KG_NODES_PATH = REPO_ROOT / "data" / "knowledge_graph" / "statutory_kg_nodes.jsonl"
KG_EDGES_PATH = REPO_ROOT / "data" / "knowledge_graph" / "statutory_kg_edges.jsonl"
MINILM_LOCAL_PATH = REPO_ROOT / "models" / "all-MiniLM-L6-v2"

ENACTMENT_ID = "pd_1869_1983"
ENACTMENT_NUMBER = "PRESIDENTIAL DECREE No. 1869 July 11, 1983"
ENACTMENT_TITLE = (
    "CONSOLIDATING AND AMENDING PRESIDENTIAL DECREE NOS. 1067-A, 1067-B, 1067-C, "
    "1399 AND 1632, RELATIVE TO THE FRANCHISE AND POWERS OF THE PHILIPPINE "
    "AMUSEMENT AND GAMING CORPORATION (PAGCOR)"
)
EXPECTED_OLD_NATIONAL_LIMIT = 164620

SEC_START_RE = re.compile(r"^(?:SECTION|SEC\.)\s+(\d+)\.\s*(.*)$")
TITLE_BANNER_RE = re.compile(r"^TITLE\s+[IVX]+\s+-")
CLOSING_DONE_RE = re.compile(r"^DONE in the City of Manila,")


def parse_pd_1869_sections(transcript_text: str) -> list:
    """Parses the 20 verbatim sections of PD 1869 into structured corpus records."""
    lines = transcript_text.splitlines()
    sections_raw = []
    cur_num = None
    cur_lines = []

    for raw_line in lines:
        line = raw_line.strip()
        if CLOSING_DONE_RE.match(line):
            break
        m = SEC_START_RE.match(line)
        if m:
            if cur_num is not None:
                sections_raw.append((cur_num, "\n".join(cur_lines).strip()))
            cur_num = int(m.group(1))
            cur_lines = [m.group(2).strip()] if m.group(2).strip() else []
            continue
        if cur_num is not None:
            if TITLE_BANNER_RE.match(line):
                continue
            cur_lines.append(line)

    if cur_num is not None:
        sections_raw.append((cur_num, "\n".join(cur_lines).strip()))

    if [num for num, _ in sections_raw] != list(range(1, 21)):
        raise ValueError(f"Expected sections 1..20, parsed {[num for num, _ in sections_raw]}")

    records = []
    for sec_num, full_block in sections_raw:
        # Collapse blank lines within multi-paragraph blocks cleanly while keeping paragraph breaks
        block = re.sub(r"\n{3,}", "\n\n", full_block).strip()
        if sec_num == 1:
            # Format: "Declaration of Policy. It is hereby declared..."
            dot_idx = block.find(".")
            if dot_idx == -1:
                raise ValueError("Malformed Section 1 heading")
            sec_title = block[:dot_idx].strip()
            body = block[dot_idx + 1:].strip()
        elif sec_num == 2:
            # Format: "- Philippine Amusement and Gaming Corporation (PAGCOR); Creation and Purpose - To implement..."
            cleaned = block.lstrip("- ").strip()
            sep_idx = cleaned.find(" - ")
            if sep_idx == -1:
                raise ValueError("Malformed Section 2 heading")
            sec_title = re.sub(r"\s+", " ", cleaned[:sep_idx]).strip()
            body = cleaned[sep_idx + 3:].strip()
        else:
            # Format: "<Title> -\n<body>" or "<Title> - <body>"
            sep_match = re.search(r"\s-\s*(?:\n|$|\s)", block)
            if not sep_match:
                raise ValueError(f"Could not separate section_title from body in Section {sec_num}")
            sec_title = re.sub(r"\s+", " ", block[:sep_match.start()]).strip()
            body = block[sep_match.end():].strip()

        sec_label = f"Section {sec_num}"
        prepended = f"[{ENACTMENT_NUMBER}: {ENACTMENT_TITLE} | {sec_label}: {sec_title}] {body}"
        wc = len(body.split())
        est_tok = int(round(wc * 1.33))
        is_bp = sec_num in (19, 20)
        records.append({
            "provision_id": f"nat_{ENACTMENT_ID}_sec_{sec_num}",
            "jurisdiction": "national",
            "enactment_id": ENACTMENT_ID,
            "enactment_number": ENACTMENT_NUMBER,
            "enactment_title": ENACTMENT_TITLE,
            "year": 1983,
            "era": "Post-War & Martial Law Era (1946–1986)",
            "section_number": sec_label,
            "section_title": sec_title,
            "raw_text": body,
            "prepended_text": prepended,
            "word_count": wc,
            "est_tokens": est_tok,
            "fits_512": est_tok <= 512,
            "is_boilerplate": is_bp,
            "is_operative": not is_bp,
            "macro_domain_id": 1,
            "macro_domain": "Executive Issuances & Policy Reorganization",
        })
    return records


def update_kg_files(records: list):
    """Idempotently appends PD 1869 enactment/provision nodes and statutory edges."""
    existing_nodes = set()
    with open(KG_NODES_PATH, "r", encoding="utf-8") as fn:
        for line in fn:
            if line.strip():
                existing_nodes.add(json.loads(line).get("id"))

    total_words = sum(r["word_count"] for r in records)
    new_nodes = []
    if ENACTMENT_ID not in existing_nodes:
        new_nodes.append({
            "id": ENACTMENT_ID,
            "node_type": "enactment",
            "jurisdiction": "national",
            "number": ENACTMENT_NUMBER,
            "category": "Presidential Decrees",
            "year": 1983,
            "title": ENACTMENT_TITLE,
            "domain": "Executive Issuances & Policy Reorganization",
            "word_count": total_words,
        })
    for r in records:
        if r["provision_id"] not in existing_nodes:
            new_nodes.append({
                "id": r["provision_id"],
                "node_type": "provision",
                "section_number": r["section_number"],
                "is_operative": r["is_operative"],
                "is_boilerplate": r["is_boilerplate"],
                "est_tokens": r["est_tokens"],
                "jurisdiction": "national",
            })

    if new_nodes:
        with open(KG_NODES_PATH, "a", encoding="utf-8") as fn:
            for node in new_nodes:
                fn.write(json.dumps(node, ensure_ascii=False) + "\n")
    print(f"[KG Nodes] Appended {len(new_nodes)} new nodes.")

    existing_edges = set()
    with open(KG_EDGES_PATH, "r", encoding="utf-8") as fe:
        for line in fe:
            if line.strip():
                e = json.loads(line)
                rel = e.get("relation") or e.get("type") or e.get("edge_type") or ""
                existing_edges.add((e.get("source"), e.get("target"), rel))

    desired_edges = []
    for r in records:
        desired_edges.append({"source": ENACTMENT_ID, "target": r["provision_id"], "relation": "CONTAINS", "weight": 1.0})
    for tgt_eid in ("pd_1399_1978", "pd_1632_1979"):
        if tgt_eid in existing_nodes:
            desired_edges.append({"source": ENACTMENT_ID, "target": tgt_eid, "relation": "AMENDS", "weight": 1})
    for src_eid in ("eo_260_1987", "ra_9487_2007"):
        if src_eid in existing_nodes:
            desired_edges.append({"source": src_eid, "target": ENACTMENT_ID, "relation": "AMENDS", "weight": 1})
    if "pd_1416_1978" in existing_nodes:
        desired_edges.append({"source": ENACTMENT_ID, "target": "pd_1416_1978", "relation": "CITES_AUTHORITY", "weight": 1})

    edges_to_append = [
        e for e in desired_edges if (e["source"], e["target"], e["relation"]) not in existing_edges
    ]
    if edges_to_append:
        with open(KG_EDGES_PATH, "a", encoding="utf-8") as fe:
            for e in edges_to_append:
                fe.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"[KG Edges] Appended {len(edges_to_append)} new edges.")


def main():
    if not VERBATIM_PATH.exists():
        raise FileNotFoundError(f"Missing transcript: {VERBATIM_PATH}")

    transcript = VERBATIM_PATH.read_text(encoding="utf-8")
    records = parse_pd_1869_sections(transcript)
    print(f"[Parse] Parsed {len(records)} PD 1869 sections:")
    for r in records:
        print(f"  {r['provision_id']}: title={r['section_title']!r} | words={r['word_count']} | est_tok={r['est_tokens']} | fits_512={r['fits_512']} | bp={r['is_boilerplate']}")

    # Idempotency check on master JSONL
    already_present = False
    leading_national = 0
    saw_non_national = False
    total_lines = 0
    with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total_lines += 1
            obj = json.loads(line)
            if obj.get("provision_id") == "nat_pd_1869_1983_sec_1":
                already_present = True
            jur = obj.get("jurisdiction")
            if jur == "national":
                if saw_non_national:
                    raise RuntimeError("Found 'national' row after non-national row!")
                leading_national += 1
            else:
                saw_non_national = True

    if already_present:
        print(f"[Idempotent] PD 1869 already present in {UNIFIED_PATH} (leading national rows={leading_national:,}, total={total_lines:,}). Skipping splice.")
        update_kg_files(records)
        return

    if leading_national != EXPECTED_OLD_NATIONAL_LIMIT:
        raise RuntimeError(f"Expected {EXPECTED_OLD_NATIONAL_LIMIT} leading national rows, found {leading_national}")

    # 1. Atomic splice into unified_dual_statutory_provisions.jsonl
    tmp_jsonl = UNIFIED_PATH.with_suffix(".jsonl.tmp")
    written = 0
    with open(UNIFIED_PATH, "r", encoding="utf-8") as fin, open(tmp_jsonl, "w", encoding="utf-8") as fout:
        for idx, line in enumerate(fin):
            if idx == EXPECTED_OLD_NATIONAL_LIMIT:
                for rec in records:
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    written += 1
            fout.write(line)
            written += 1
    os.replace(tmp_jsonl, UNIFIED_PATH)
    print(f"[JSONL] Spliced 20 PD 1869 rows at index {EXPECTED_OLD_NATIONAL_LIMIT:,} -> new total={written:,} rows (national=164,640).")

    # 2. Splice 20 MiniLM vectors into dual_corpus_embeddings_minilm.npy
    torch.set_num_threads(4)
    if MINILM_LOCAL_PATH.exists():
        model = SentenceTransformer(str(MINILM_LOCAL_PATH), device="cpu")
    else:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    model.max_seq_length = 256
    new_vecs = model.encode(
        [r["prepended_text"] for r in records],
        batch_size=20,
        show_progress_bar=False,
        normalize_embeddings=True,
    ).astype(np.float32)
    assert new_vecs.shape == (20, 384), f"Unexpected encoded shape: {new_vecs.shape}"

    old_emb = np.load(str(EMB_PATH))
    if old_emb.shape != (176421, 384):
        raise RuntimeError(f"Unexpected embeddings shape before splice: {old_emb.shape}")
    spliced_emb = np.concatenate(
        [old_emb[:EXPECTED_OLD_NATIONAL_LIMIT], new_vecs, old_emb[EXPECTED_OLD_NATIONAL_LIMIT:]],
        axis=0,
    ).astype(np.float32)
    assert spliced_emb.shape == (176441, 384), f"Unexpected spliced shape: {spliced_emb.shape}"

    tmp_npy = EMB_PATH.with_name(EMB_PATH.name + ".tmp.npy")
    np.save(str(tmp_npy), spliced_emb)
    os.replace(tmp_npy, EMB_PATH)
    print(f"[Embeddings] Spliced 20 MiniLM vectors -> {EMB_PATH} shape={spliced_emb.shape} dtype={spliced_emb.dtype}")

    # 3. Update dual_corpus_embeddings_meta.json atomically
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    new_pids = [r["provision_id"] for r in records]
    old_pids = meta["provision_ids"]
    meta["provision_ids"] = old_pids[:EXPECTED_OLD_NATIONAL_LIMIT] + new_pids + old_pids[EXPECTED_OLD_NATIONAL_LIMIT:]
    meta["total_provisions"] = len(meta["provision_ids"])
    meta["national_count"] = int(meta.get("national_count", EXPECTED_OLD_NATIONAL_LIMIT)) + len(records)
    meta["operative_count"] = int(meta.get("operative_count", 172780)) + sum(1 for r in records if r["is_operative"])
    meta["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    tmp_meta = META_PATH.with_suffix(".json.tmp")
    tmp_meta.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_meta, META_PATH)
    print(f"[Meta] Updated {META_PATH}: total={meta['total_provisions']:,}, national={meta['national_count']:,}")

    # 4. Update KG nodes & edges
    update_kg_files(records)

    # 5. Rebuild BM25 index & delete stale CSR cache so app.py rebuilds it cleanly
    print("[BM25] Rebuilding dual_corpus_bm25.pkl...")
    res = subprocess.run([sys.executable, str(BM25_BUILD_SCRIPT)], cwd=str(REPO_ROOT), check=True)
    if res.returncode == 0:
        for stale in (BM25_CSR_PATH, BM25_VOCAB_PATH):
            if stale.exists():
                stale.unlink()
                print(f"[BM25] Removed stale cache {stale.name}")

    print("[DONE] PD 1869 ingestion completed cleanly.")


if __name__ == "__main__":
    main()
