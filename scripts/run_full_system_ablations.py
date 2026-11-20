"""
scripts/run_full_system_ablations.py
====================================
Unified Stage-by-Stage Ablation & Synchronized Full-PDF Audit Runner
across Tier 2 (N = 6 Folio Drafts) and Tier 3 (N = 10 Authentic Cases).

Uses the upgraded dynamic production engine in src/demo/app.py:
  - Exact sparse CSR BM25 (240x faster, identical BM25Okapi math)
  - Stage 2 (premise, hypothesis) pair deduplication cache
  - Genuine Statutory KG topological distance d_G lookup (zero hardcoded elifs)
  - General Dynamic Numeric-Bound Verifier (zero hardcoded P5,000 / statute IDs)

Ablation Variants:
  V0_isolated_stage2         : Stage 1 bypassed (direct target-law pairs: Static 0.45, KG tau*, +Numeric)
  V1_bm25_only               : Stage 1 = BM25 only          | Stage 2 = DeBERTa + KG tau* + Numeric
  V2_minilm_only             : Stage 1 = MiniLM only        | Stage 2 = DeBERTa + KG tau* + Numeric
  V3_hybrid_pure_neural      : Stage 1 = BM25 + MiniLM      | Stage 2 = DeBERTa only (static tau = 0.45)
  V4_hybrid_neural_kg_tau    : Stage 1 = BM25 + MiniLM      | Stage 2 = DeBERTa + Real KG tau*(u,v)
  V5_full_system             : Stage 1 = BM25 + MiniLM      | Stage 2 = DeBERTa + Real KG tau*(u,v) + Numeric
  V6_hybrid_kg_expansion     : Stage 1 = Hybrid + 1-Hop KG  | Stage 2 = DeBERTa + Real KG tau*(u,v) + Numeric

Usage:
  $env:TORCH_NUM_THREADS="6"; .\\venv\\Scripts\\python.exe scripts/run_full_system_ablations.py --suite tier2
  $env:TORCH_NUM_THREADS="6"; .\\venv\\Scripts\\python.exe scripts/run_full_system_ablations.py --suite tier3_std8
  $env:TORCH_NUM_THREADS="6"; .\\venv\\Scripts\\python.exe scripts/run_full_system_ablations.py --suite tier3_revcode
"""

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("TORCH_NUM_THREADS", "6")

import numpy as np
import pypdf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "demo"))
import app as demo_app  # noqa: E402

UNIFIED_PATH = REPO_ROOT / "data" / "unified_dual_statutory_provisions.jsonl"
KG_EDGES_PATH = REPO_ROOT / "data" / "knowledge_graph" / "statutory_kg_edges.jsonl"
TIER2_BENCHMARK_PATH = REPO_ROOT / "ground_truth" / "tier2_synthetic_drafts" / "tier2_draft_ordinances_benchmark.jsonl"
TIER2_PDF_DIR = REPO_ROOT / "ground_truth" / "tier2_synthetic_drafts" / "tier2_draft_ordinances_pdf"
TIER3_CASES_PATH = REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_jurisprudential_cases.jsonl"
TIER3_PDF_DIR = REPO_ROOT / "src" / "demo" / "sample_cases" / "pdf"

OUT_TIER2_ABL = REPO_ROOT / "output" / "tier2_full_ablation_authentic.json"
OUT_TIER2_SYNC_JSON = REPO_ROOT / "output" / "tier2_live_demo_full_audit_all6.json"
OUT_TIER2_SYNC_TXT = REPO_ROOT / "output" / "tier2_live_demo_audit_report.txt"

OUT_TIER3_STD8_ABL = REPO_ROOT / "output" / "tier3_standard8_full_ablation_authentic.json"
OUT_TIER3_FULL_ABL = REPO_ROOT / "output" / "tier3_full_ablation_authentic.json"
OUT_TIER3_SYNC_JSON = REPO_ROOT / "output" / "tier3_live_demo_full_audit_all10.json"
OUT_TIER3_SYNC_TXT = REPO_ROOT / "output" / "tier3_live_demo_audit_report.txt"


def get_national_corpus_limit() -> int:
    if getattr(demo_app.NEURAL_ENGINE, "national_corpus_limit", 0) > 0:
        return int(demo_app.NEURAL_ENGINE.national_corpus_limit)
    limit = 0
    with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            if json.loads(line).get("jurisdiction") == "national":
                limit += 1
            else:
                break
    return limit

TIER3_CASES = [
    ("DAVAO-TIER3-01", "01_mosqueda_aerial_spraying_ban.pdf"),
    ("DAVAO-TIER3-02", "02_evasco_billboard_regulation.pdf"),
    ("DAVAO-TIER3-03", "03_arc_investors_holding_tax.pdf"),
    ("DAVAO-TIER3-04", "04_first_meridian_payment_under_protest.pdf"),
    ("DAVAO-TIER3-05", "05_davao_gsis_property_tax.pdf"),
    ("DAVAO-TIER3-06", "06_mining_ban_watershed.pdf"),
    ("DAVAO-TIER3-07", "07_davao_anti_smoking_stricter_standard.pdf"),
    ("DAVAO-TIER3-08", "08_davao_speed_limits_traffic_code.pdf"),
    ("SC-PHIL-09", "09_magtajas_casino_preemption.pdf"),
    ("SC-PHIL-10", "10_city_of_manila_laguio_due_process.pdf"),
]

TIER2_TARGET_PIDS = {
    ("DRAFT-ORD-2026-01", 9): ["nat_ra_8485_1998_sec_6", "nat_ra_9482_2007_sec_7"],
    ("DRAFT-ORD-2026-01", 13): ["nat_ra_7160_1991_sec_458"],
    ("DRAFT-ORD-2026-02", 8): ["nat_ra_10173_2012_sec_13", "nat_ra_10173_2012_sec_16"],
    ("DRAFT-ORD-2026-03", 4): ["nat_ra_10121_2010_sec_21", "nat_ra_7160_1991_sec_324"],
    ("DRAFT-ORD-2026-04", 8): ["nat_ra_7160_1991_sec_133", "nat_ra_7160_1991_sec_192"],
    ("DRAFT-ORD-2026-05", 4): ["nat_ra_7160_1991_sec_133", "nat_ra_7160_1991_sec_21"],
    ("DRAFT-ORD-2026-06", 4): ["nat_ra_7160_1991_sec_20", "nat_ra_6657_1988_sec_65", "nat_eo_124_1993_sec_1"],
}

XAI_SPAN_RE = re.compile(
    r'<span[^>]*class="xai-token"[^>]*data-weight="([^"]+)"[^>]*>(.*?)</span>',
    re.DOTALL,
)


def extract_top_xai_tokens(xai_html: str, top_k: int = 15):
    if not xai_html:
        return []
    tokens = []
    for weight_str, raw_tok in XAI_SPAN_RE.findall(xai_html):
        tok = html.unescape(raw_tok).strip()
        if not tok:
            continue
        try:
            w = float(weight_str)
        except ValueError:
            continue
        tokens.append((tok, round(w, 4)))
    tokens.sort(key=lambda x: x[1], reverse=True)
    seen = set()
    unique_top = []
    for tok, w in tokens:
        k = tok.lower()
        if k not in seen:
            seen.add(k)
            unique_top.append({"token": tok, "weight": w})
        if len(unique_top) >= top_k:
            break
    return unique_top


def is_obsolete_colonial(eid: str = "", citation: str = "") -> bool:
    e_low = (eid or "").lower()
    c_low = (citation or "").lower()
    if e_low.startswith(("act_", "ca_", "commonwealth_act_", "ra_4354_")):
        return True
    if c_low.startswith(("act no.", "act_", "commonwealth act", "commonwealth_act")) or "4354" in c_low:
        return True
    return False


def normalize_verdict(v: str) -> str:
    v_up = (v or "").upper()
    if "CONTRADICTION" in v_up:
        return "Contradiction"
    if "ENTAILMENT" in v_up:
        return "Entailment"
    return "Neutral"


def extract_conflict_pairs_from_sections(sections: list):
    conflict_pairs = []
    for sec in sections:
        if sec.get("is_boilerplate"):
            continue
        cands = sec.get("candidate_shortlist") or []
        sec_conflicts = []
        for c in cands:
            if not c.get("stage2_evaluated"):
                continue
            if c.get("is_conflict"):
                sec_conflicts.append(c)

        if sec_conflicts:
            sec_conflicts.sort(key=lambda x: x.get("stage2_confidence") or 0, reverse=True)
            for c in sec_conflicts:
                ord_html = c.get("ordinance_html") or sec.get("ordinance_html") or ""
                stat_html = c.get("statute_html") or sec.get("statute_html") or ""
                conflict_pairs.append({
                    "sec_num": sec.get("sec_num"),
                    "sec_title": sec.get("sec_title"),
                    "target_statute": c.get("citation") or sec.get("target_statute"),
                    "statute_title": c.get("title") or sec.get("statute_title") or "",
                    "confidence_pct": c.get("stage2_confidence") if c.get("stage2_confidence") is not None else round((c.get("p_contradiction") or 0.95) * 100, 2),
                    "p_contradiction": c.get("p_contradiction"),
                    "dynamic_threshold_pct": c.get("dynamic_threshold_pct", 45.0),
                    "graph_distance_d_g": c.get("graph_distance_d_g", sec.get("graph_distance_d_g", 999)),
                    "relation_type": c.get("relation_type", sec.get("relation_type", "")),
                    "numeric_bound_breach": c.get("numeric_bound_breach"),
                    "kg_expanded": bool(c.get("kg_expanded", False)),
                    "kg_path": c.get("kg_path", ""),
                    "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                    "statute_text": (c.get("raw_text") or c.get("prepended_text") or sec.get("statute_text") or "").strip(),
                    "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                    "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                    "legal_rationale": c.get("summary") or sec.get("legal_rationale"),
                })
        elif sec.get("verdict") == "CONTRADICTION":
            ord_html = sec.get("ordinance_html") or ""
            stat_html = sec.get("statute_html") or ""
            conflict_pairs.append({
                "sec_num": sec.get("sec_num"),
                "sec_title": sec.get("sec_title"),
                "target_statute": sec.get("target_statute"),
                "statute_title": sec.get("statute_title") or "",
                "confidence_pct": sec.get("confidence_percentage", 95.0),
                "p_contradiction": sec.get("conflict_probability"),
                "dynamic_threshold_pct": sec.get("dynamic_threshold_pct", 45.0),
                "graph_distance_d_g": sec.get("graph_distance_d_g", 999),
                "relation_type": sec.get("relation_type", ""),
                "numeric_bound_breach": None,
                "kg_expanded": False,
                "kg_path": "",
                "ordinance_text": (sec.get("ordinance_text") or sec.get("text") or "").strip(),
                "statute_text": (sec.get("statute_text") or "").strip(),
                "top_ordinance_xai": extract_top_xai_tokens(ord_html, top_k=15),
                "top_statute_xai": extract_top_xai_tokens(stat_html, top_k=15),
                "legal_rationale": sec.get("legal_rationale"),
            })
    return conflict_pairs


def derive_stage2_variant_sections(sections_v5: list, use_kg_threshold: bool, use_numeric_bounds: bool) -> list:
    """
    Exact mathematical derivation of Stage 2 variants (V3: static 0.45 no numeric;
    V4: KG dynamic tau* no numeric) directly from V5's audited sections without
    re-running identical Stage 1 or XAI passes.
    """
    derived = []
    for sec in sections_v5:
        if sec.get("is_boilerplate"):
            derived.append(dict(sec))
            continue

        sec_copy = dict(sec)
        cands = [dict(c) for c in (sec.get("candidate_shortlist") or [])]
        eval_cands = [c for c in cands if c.get("stage2_evaluated")]

        conflict_cands = []
        for c in eval_cands:
            p_c = float(c.get("p_contradiction", 0.0))
            tau_c = float(c.get("dynamic_threshold", 0.45)) if use_kg_threshold else 0.45
            has_num = bool((c.get("numeric_bound_breach") or {}).get("breached")) if use_numeric_bounds else False
            is_c = (p_c >= tau_c) or has_num
            c["is_conflict"] = is_c
            c["dynamic_threshold"] = tau_c
            c["dynamic_threshold_pct"] = round(tau_c * 100.0, 1)
            if not use_kg_threshold:
                c["graph_distance_d_g"] = 999
                c["relation_type"] = "Static Baseline (tau=0.45)"
            if not use_numeric_bounds:
                c["numeric_bound_breach"] = None
                c["stage2_confidence"] = round(p_c * 100.0, 1)
            if is_c:
                eff = max(p_c, 0.95) if has_num else p_c
                conflict_cands.append((eff, c))

        if conflict_cands:
            conflict_cands.sort(key=lambda x: x[0], reverse=True)
            eff_top, pri = conflict_cands[0]
            sec_copy["verdict"] = "CONTRADICTION"
            sec_copy["target_statute"] = pri.get("citation")
            sec_copy["confidence_percentage"] = round(eff_top * 100.0, 1)
        else:
            pri = eval_cands[0] if eval_cands else None
            p_e = float(pri.get("p_entailment", 0.0)) if pri else 0.0
            p_c = float(pri.get("p_contradiction", 0.0)) if pri else 0.0
            if p_e >= 0.45 and p_e > p_c:
                sec_copy["verdict"] = "ENTAILMENT"
            else:
                sec_copy["verdict"] = "NEUTRAL"
        sec_copy["candidate_shortlist"] = cands
        derived.append(sec_copy)
    return derived


class UnifiedCorpusAndKG:
    """Indexes national operative provisions and 1-hop KG adjacency (CITES_AUTHORITY, AMENDS)."""

    def __init__(self):
        t0 = time.perf_counter()
        self.pid_to_row = {}
        self.row_to_pid = {}
        self.row_to_eid = {}
        self.eid_to_op_rows = defaultdict(list)
        self.records_by_pid = {}
        self.national_corpus_limit = get_national_corpus_limit()

        needed_pids = {pid for plist in TIER2_TARGET_PIDS.values() for pid in plist}
        if TIER3_CASES_PATH.exists():
            with open(TIER3_CASES_PATH, "r", encoding="utf-8") as ft3:
                for line in ft3:
                    if line.strip():
                        for pid in json.loads(line).get("target_provision_ids", []):
                            needed_pids.add(pid)

        with open(UNIFIED_PATH, "r", encoding="utf-8") as f:
            for row_idx, line in enumerate(f):
                if row_idx >= self.national_corpus_limit:
                    break
                rec = json.loads(line)
                pid = rec.get("provision_id")
                eid = rec.get("enactment_id") or ""
                en_num = rec.get("enactment_number") or ""
                if pid in needed_pids:
                    self.records_by_pid[pid] = rec
                if pid:
                    self.pid_to_row[pid] = row_idx
                    self.row_to_pid[row_idx] = pid
                self.row_to_eid[row_idx] = eid
                if not is_obsolete_colonial(eid, en_num) and not rec.get("is_boilerplate", False):
                    self.eid_to_op_rows[eid].append(row_idx)

        self.kg_adj = defaultdict(set)
        self.kg_edge_reasons = defaultdict(list)
        self.edge_counts = defaultdict(int)
        with open(KG_EDGES_PATH, "r", encoding="utf-8") as f:
            for line in f:
                e = json.loads(line)
                rel = e.get("relation") or e.get("type") or e.get("edge_type") or ""
                if rel not in ("CITES_AUTHORITY", "AMENDS"):
                    continue
                s = str(e.get("source") or "")
                t = str(e.get("target") or "")
                if is_obsolete_colonial(s) or is_obsolete_colonial(t):
                    continue
                if s not in self.eid_to_op_rows or t not in self.eid_to_op_rows:
                    continue
                self.edge_counts[rel] += 1
                self.kg_adj[s].add(t)
                self.kg_adj[t].add(s)
                self.kg_edge_reasons[(s, t)].append(f"{s} --[{rel}]--> {t}")
                self.kg_edge_reasons[(t, s)].append(f"{s} --[{rel}]--> {t}")

        print(f"[CorpusKG] Indexed {len(self.pid_to_row):,} national provisions, {len(self.eid_to_op_rows):,} enactments, KG={dict(self.edge_counts)} in {time.perf_counter()-t0:.2f}s", flush=True)

    def format_candidate(self, item: dict, rank: int, sim_score: float, kg_path: str) -> dict:
        enact_num = item.get("enactment_number") or item.get("enactment_id") or "Statute"
        sec_num = item.get("section_number") or ""
        sec_title = item.get("section_title") or ""
        cit = f"{enact_num} {sec_num}".strip()
        raw_txt = item.get("raw_text", "")
        prep_txt = item.get("prepended_text") or raw_txt
        raw_title = (item.get("enactment_title") or "").strip()
        clean_title = raw_title if len(raw_title) >= 8 and raw_title.upper() not in ("MANILA", "DAVAO", "PHILIPPINES") else enact_num
        sec_display = f"{sec_num}. {sec_title}" if (sec_num and sec_title) else (sec_num or sec_title or "Operative Provision")
        return {
            "rank": rank,
            "provision_id": item.get("provision_id"),
            "enactment_id": item.get("enactment_id"),
            "citation": cit,
            "title": clean_title,
            "section_title": sec_display,
            "section": sec_display,
            "jurisdiction": "National Statute",
            "raw_text": raw_txt,
            "prepended_text": prep_txt,
            "similarity": round(float(sim_score), 4),
            "score": round(float(sim_score), 4),
            "stage1_score": round(float(sim_score), 4),
            "similarity_score": round(float(sim_score), 4),
            "lawphil_url": demo_app.get_lawphil_url(cit, "national"),
            "kg_expanded": True,
            "kg_path": kg_path,
        }


def run_kg_expansion_on_audit(
    raw_text: str,
    pdf_name: str,
    data_v5: dict,
    corpus_kg: UnifiedCorpusAndKG,
    only_sec_nums: set = None,
) -> tuple:
    """
    Runs V6_hybrid_kg_expansion on top of V5's baseline Stage 1 Top-8 by expanding 1-hop KG
    neighbors (CITES_AUTHORITY + AMENDS) from N_cite(D) union Stage 1 Top-8, scoring with
    exact Stage 1 hybrid formula (0.50*norm_BM25 + 0.50*Dense), evaluating Top-M=8 new candidates
    via DeBERTa-v3 (cached), real KG tau*(u,v), and Dynamic Numeric-Bound Verifier.
    """
    doc_title, chunks = demo_app.chunk_ordinance_sections(raw_text, default_title=pdf_name)
    chunk_by_num = {c["sec_num"]: c for c in chunks}
    doc_cited_eids = demo_app.extract_cited_enactment_ids(raw_text)
    nat_limit = corpus_kg.national_corpus_limit
    nat_emb = demo_app.NEURAL_ENGINE.statutory_embeddings[:nat_limit]

    t_s1 = 0.0
    t_s2 = 0.0
    aug_sections = []

    with open(UNIFIED_PATH, "rb") as f_uni:
        for sec in data_v5.get("sections", []):
            s_num = sec["sec_num"]
            if only_sec_nums is not None and s_num not in only_sec_nums:
                continue
            if sec.get("is_boilerplate"):
                aug_sections.append(dict(sec))
                continue

            ch = chunk_by_num[s_num]
            s_marker = ch.get("sec_marker") or f"SECTION {s_num}"
            header_title = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
            query_str = f"[{doc_title} | {header_title}] {ch['text']}"
            hypothesis_text = f"[{header_title}] {ch['text']}"

            cands_50 = sec.get("candidate_shortlist") or []
            base_eval = [dict(c) for c in cands_50 if c.get("stage2_evaluated")]
            already_pids = {c.get("provision_id") for c in base_eval if c.get("provision_id")}
            already_cits = {c.get("citation") for c in base_eval if c.get("citation")}

            seed_eids = set(doc_cited_eids)
            seed_origins = {eid: "N_cite(D)" for eid in doc_cited_eids}
            for bc in base_eval:
                bpid = bc.get("provision_id")
                if bpid and bpid in corpus_kg.pid_to_row:
                    beid = corpus_kg.row_to_eid[corpus_kg.pid_to_row[bpid]]
                    if beid and not is_obsolete_colonial(beid):
                        seed_eids.add(beid)
                        seed_origins.setdefault(beid, f"Stage1 Top-8 ({bc.get('citation')})")

            e_kg = set(seed_eids)
            eid_path_map = {eid: seed_origins[eid] for eid in seed_eids}
            for seid in seed_eids:
                for nb in corpus_kg.kg_adj.get(seid, ()):
                    if nb not in e_kg:
                        e_kg.add(nb)
                        reasons = corpus_kg.kg_edge_reasons.get((seid, nb), [f"{seid} <-> {nb}"])
                        eid_path_map[nb] = f"{seed_origins[seid]} -> {reasons[0]}"

            kg_rows = []
            for eid in e_kg:
                for r_idx in corpus_kg.eid_to_op_rows.get(eid, ()):
                    if corpus_kg.row_to_pid.get(r_idx) not in already_pids:
                        kg_rows.append(r_idx)

            t0 = time.perf_counter()
            new_kg_cands = []
            if kg_rows:
                q_emb = demo_app.NEURAL_ENGINE.embedder.encode([query_str], normalize_embeddings=True)[0]
                kg_arr = np.array(kg_rows, dtype=np.int64)
                dense_kg = np.dot(nat_emb[kg_arr], q_emb)

                clean_q = re.sub(r"[^a-zA-Z0-9\s]", " ", query_str.lower())
                q_tokens = [w for w in clean_q.split() if len(w) > 2]
                bm_scope = demo_app.NEURAL_ENGINE.score_bm25(q_tokens, scope_limit=nat_limit) if q_tokens else None
                if bm_scope is not None:
                    max_bm = float(np.max(bm_scope))
                    norm_bm_kg = (bm_scope[kg_arr] / max_bm) if max_bm > 0 else bm_scope[kg_arr]
                    hybrid_kg = (0.50 * norm_bm_kg) + (0.50 * dense_kg)
                else:
                    hybrid_kg = dense_kg

                top_local = np.argpartition(hybrid_kg, -min(16, len(hybrid_kg)))[-min(16, len(hybrid_kg)):]
                top_local = top_local[np.argsort(-hybrid_kg[top_local])]
                for o_i in top_local:
                    if len(new_kg_cands) >= 8:
                        break
                    r_idx = int(kg_rows[o_i])
                    f_uni.seek(demo_app.NEURAL_ENGINE.provision_offsets[r_idx])
                    item = json.loads(f_uni.readline().decode("utf-8"))
                    eid = item.get("enactment_id", "")
                    cand = corpus_kg.format_candidate(item, 8 + len(new_kg_cands) + 1, float(hybrid_kg[o_i]), eid_path_map.get(eid, "KG 1-hop"))
                    if cand["citation"] not in already_cits:
                        new_kg_cands.append(cand)
            t_s1 += time.perf_counter() - t0

            t1 = time.perf_counter()
            if new_kg_cands:
                pairs = [
                    (f"[{c['citation']}] {(c.get('raw_text') or c.get('prepended_text', '')).lstrip('- \r\n')}".strip(), hypothesis_text)
                    for c in new_kg_cands
                ]
                res_list = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(pairs)
                for cand, res in zip(new_kg_cands, res_list):
                    cand["stage2_evaluated"] = True
                    cand["p_contradiction"] = res["p_contradiction"]
                    cand["p_entailment"] = res["p_entailment"]
                    cand["p_neutral"] = res["p_neutral"]
                    cand["stage2_confidence"] = round(res["p_contradiction"] * 100.0, 1)
                    c_raw = cand.get("raw_text") or cand.get("prepended_text", "")
                    d_g, dom, rel_t = demo_app.compute_topological_distance(cand["citation"], ch["text"], c_raw, draft_cited_eids=doc_cited_eids)
                    tau_dyn = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
                    cand["graph_distance_d_g"] = d_g
                    cand["domain"] = dom
                    cand["relation_type"] = rel_t
                    cand["dynamic_threshold"] = tau_dyn
                    cand["dynamic_threshold_pct"] = round(tau_dyn * 100.0, 1)
                    num_chk = demo_app.verify_dynamic_numeric_bounds(c_raw, ch["text"])
                    has_num = bool(num_chk.get("breached"))
                    cand["numeric_bound_breach"] = num_chk if has_num else None
                    is_c = (res["p_contradiction"] >= tau_dyn) or has_num
                    if has_num:
                        cand["stage2_confidence"] = max(cand["stage2_confidence"], 95.0)
                    cand["is_conflict"] = is_c
                    if is_c:
                        cand["summary"] = num_chk["detail"] if (has_num and res["p_contradiction"] < tau_dyn) else (
                            f"DeBERTa-v3 ({cand['stage2_confidence']}% vs tau*={tau_dyn:.3f}, d_G={d_g})"
                        )
                        c_xai = demo_app.NEURAL_ENGINE.extract_cross_attention_attribution(c_raw, ch["text"])
                        cand["statute_html"] = c_xai["statute_html"]
                        cand["ordinance_html"] = c_xai["ordinance_html"]
            t_s2 += time.perf_counter() - t1

            aug_eval = base_eval + new_kg_cands
            sec_copy = dict(sec)
            sec_copy["candidate_shortlist"] = aug_eval
            confs = [
                (max(c.get("p_contradiction", 0.0), 0.95) if (c.get("numeric_bound_breach") or {}).get("breached") else c.get("p_contradiction", 0.0), c)
                for c in aug_eval if c.get("is_conflict")
            ]
            if confs:
                confs.sort(key=lambda x: x[0], reverse=True)
                sec_copy["verdict"] = "CONTRADICTION"
                sec_copy["target_statute"] = confs[0][1]["citation"]
                sec_copy["confidence_percentage"] = round(confs[0][0] * 100.0, 1)
            else:
                pri = base_eval[0] if base_eval else (aug_eval[0] if aug_eval else None)
                p_e = pri.get("p_entailment", 0.0) if pri else 0.0
                p_c = pri.get("p_contradiction", 0.0) if pri else 0.0
                sec_copy["verdict"] = "ENTAILMENT" if (p_e >= 0.45 and p_e > p_c) else "NEUTRAL"
            aug_sections.append(sec_copy)

    return aug_sections, round(t_s1, 2), round(t_s2, 2)


def compute_tier2_metrics(all_provs: list, doc_results: list) -> dict:
    total = len(all_provs)
    tp_c = sum(1 for p in all_provs if p["gold_label"] == "Contradiction" and p["predicted_label"] == "Contradiction")
    fp_c = sum(1 for p in all_provs if p["gold_label"] != "Contradiction" and p["predicted_label"] == "Contradiction")
    fn_c = sum(1 for p in all_provs if p["gold_label"] == "Contradiction" and p["predicted_label"] != "Contradiction")
    tn_c = sum(1 for p in all_provs if p["gold_label"] != "Contradiction" and p["predicted_label"] != "Contradiction")

    prec = (tp_c / (tp_c + fp_c)) if (tp_c + fp_c) > 0 else 0.0
    rec = (tp_c / (tp_c + fn_c)) if (tp_c + fn_c) > 0 else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    f2 = (5 * prec * rec / (4 * prec + rec)) if (4 * prec + rec) > 0 else 0.0
    spec = (tn_c / (tn_c + fp_c)) * 100.0 if (tn_c + fp_c) > 0 else 0.0
    bin_acc = ((tp_c + tn_c) / total) * 100.0 if total > 0 else 0.0

    correct_3 = sum(1 for p in all_provs if p["gold_label"] == p["predicted_label"])
    acc_3 = (correct_3 / total) * 100.0 if total > 0 else 0.0
    f1s = []
    per_cls = {}
    for cls in ("Neutral", "Entailment", "Contradiction"):
        tp = sum(1 for p in all_provs if p["gold_label"] == cls and p["predicted_label"] == cls)
        fp = sum(1 for p in all_provs if p["gold_label"] != cls and p["predicted_label"] == cls)
        fn = sum(1 for p in all_provs if p["gold_label"] == cls and p["predicted_label"] != cls)
        pr = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        rc = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        fc = (2 * pr * rc / (pr + rc)) if (pr + rc) > 0 else 0.0
        f1s.append(fc)
        per_cls[cls] = {"support": tp + fn, "tp": tp, "fp": fp, "fn": fn, "precision": round(pr, 4), "recall": round(rc, 4), "f1": round(fc, 4)}
    macro_f1 = sum(f1s) / 3.0

    exact_gold_matches = sum(p.get("exact_gold_match", 0) for p in all_provs if p["gold_label"] == "Contradiction")
    total_ui_pairs = sum(d["total_conflicts_found"] for d in doc_results)
    docs_flagged = sum(1 for d in doc_results if d["total_conflicts_found"] > 0)

    return {
        "documents_evaluated": len(doc_results),
        "provisions_evaluated": total,
        "documents_flagged": docs_flagged,
        "document_screening_recall": round((docs_flagged / len(doc_results)) * 100.0, 2) if doc_results else 0.0,
        "total_ui_conflict_pairs": total_ui_pairs,
        "exact_answer_key_statute_matches": exact_gold_matches,
        "binary_confusion_matrix": {"true_positives": tp_c, "false_positives": fp_c, "true_negatives": tn_c, "false_negatives": fn_c},
        "binary_metrics": {
            "contradiction_precision": round(prec, 4),
            "contradiction_recall": round(rec, 4),
            "contradiction_f1": round(f1, 4),
            "cost_sensitive_f2": round(f2, 4),
            "section_level_specificity_pct": round(spec, 2),
            "binary_screening_accuracy_pct": round(bin_acc, 2),
        },
        "three_class_metrics": {
            "three_class_accuracy_pct": round(acc_3, 2),
            "three_class_correct": correct_3,
            "macro_f1": round(macro_f1, 4),
            "per_class_performance": per_cls,
        },
    }


def evaluate_tier2_sections_against_gold(doc_id: str, gold_doc: dict, audited_secs: list, latency_s: float) -> tuple:
    gold_secs = {s["sec_num"]: s for s in gold_doc["sections"]}
    pairs = extract_conflict_pairs_from_sections(audited_secs)
    distinct_secs = sorted(set(p["sec_num"] for p in pairs))
    sec_evals = []
    doc_tp = 0

    for sec in audited_secs:
        s_num = sec["sec_num"]
        gs = gold_secs[s_num]
        g_lbl = gs.get("label", "Neutral")
        p_lbl = normalize_verdict(sec.get("verdict", "NEUTRAL"))
        cands = sec.get("candidate_shortlist") or []
        eval_cands = [c for c in cands if c.get("stage2_evaluated")]
        flagged_cands = [c for c in eval_cands if c.get("is_conflict")]

        exact_gold = 0
        if g_lbl == "Contradiction" and p_lbl == "Contradiction":
            doc_tp += 1
            t_pids = set(TIER2_TARGET_PIDS.get((doc_id, s_num), []))
            flagged_pids = {c.get("provision_id") for c in flagged_cands}
            if t_pids & flagged_pids:
                exact_gold = 1

        sec_evals.append({
            "doc_id": doc_id,
            "sec_num": s_num,
            "sec_title": sec.get("sec_title"),
            "is_boilerplate": bool(sec.get("is_boilerplate", False)),
            "gold_label": g_lbl,
            "predicted_label": p_lbl,
            "exact_gold_match": exact_gold,
            "flagged_pairs_count": len(flagged_cands) if flagged_cands else (1 if p_lbl == "Contradiction" else 0),
            "flagged_statutes": [c.get("citation") for c in flagged_cands],
            "retrieved_top_statute": sec.get("target_statute"),
        })

    doc_rec = {
        "doc_id": doc_id,
        "functional_typology": gold_doc.get("functional_typology", ""),
        "gold_contradictions": sum(1 for s in gold_secs.values() if s["label"] == "Contradiction"),
        "true_positive_contradictions": doc_tp,
        "total_conflicts_found": len(pairs),
        "problematic_sections": distinct_secs,
        "audit_latency_s": round(latency_s, 2),
        "conflict_pairs": pairs,
        "sections": sec_evals,
    }
    return doc_rec, sec_evals


def run_v0_isolated_ablation(corpus_kg: UnifiedCorpusAndKG) -> dict:
    """Runs V0 (Stage 1 bypassed: isolated target-law check) across Tier 2 (7 defects) & Tier 3 (10 cases)."""
    print("\n" + "=" * 88)
    print("V0 ABLATION: ISOLATED TARGET-LAW CHECK (STAGE 1 BYPASSED -> STAGE 2 ONLY)")
    print("=" * 88)

    # --- Tier 2 V0 ---
    t2_docs = {}
    with open(TIER2_BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                t2_docs[d["doc_id"]] = d

    t2_chunk_map = {}
    for doc_id in sorted(t2_docs.keys()):
        pdf_path = TIER2_PDF_DIR / f"{doc_id}.pdf"
        raw_txt = "\n\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(str(pdf_path)).pages).strip()
        _, chunks = demo_app.chunk_ordinance_sections(raw_txt, default_title=pdf_path.name)
        t2_chunk_map[doc_id] = (raw_txt, {c["sec_num"]: c for c in chunks})

    t2_pairs = []
    t2_meta = []
    for (doc_id, sec_num), pids in TIER2_TARGET_PIDS.items():
        raw_doc_txt, c_map = t2_chunk_map[doc_id]
        doc_cited = demo_app.extract_cited_enactment_ids(raw_doc_txt)
        ch = c_map[sec_num]
        s_marker = ch.get("sec_marker") or f"SECTION {sec_num}"
        hdr = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
        hyp = f"[{hdr}] {ch['text']}".strip()
        for pid in pids:
            rec = corpus_kg.records_by_pid[pid]
            cit = f"{rec.get('enactment_number') or rec.get('enactment_id')} {rec.get('section_number') or ''}".strip()
            stat_txt = (rec.get("raw_text") or "").lstrip("- \r\n")
            prem = f"[{cit}] {stat_txt}".strip()
            t2_pairs.append((prem, hyp))
            t2_meta.append((doc_id, sec_num, pid, cit, ch["text"], stat_txt, doc_cited))

    t2_res = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(t2_pairs)
    t2_per_defect = defaultdict(list)
    for meta, sc in zip(t2_meta, t2_res):
        doc_id, sec_num, pid, cit, dr_txt, st_txt, doc_cited = meta
        d_g, dom, rel = demo_app.compute_topological_distance(cit, dr_txt, st_txt, draft_cited_eids=doc_cited)
        tau_dyn = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
        num_chk = demo_app.verify_dynamic_numeric_bounds(st_txt, dr_txt)
        p_c = float(sc["p_contradiction"])
        t2_per_defect[(doc_id, sec_num)].append({
            "provision_id": pid,
            "citation": cit,
            "p_contradiction_pct": round(p_c * 100.0, 2),
            "p_entailment_pct": round(float(sc["p_entailment"]) * 100.0, 2),
            "d_g": d_g,
            "relation_type": rel,
            "tau_dyn": tau_dyn,
            "hit_static_045": p_c >= 0.45,
            "hit_kg_tau": p_c >= tau_dyn,
            "numeric_breach": num_chk if num_chk["breached"] else None,
            "hit_kg_plus_numeric": (p_c >= tau_dyn) or bool(num_chk["breached"]),
        })

    t2_defect_rows = []
    for (doc_id, sec_num), rows in t2_per_defect.items():
        best = max(rows, key=lambda r: r["p_contradiction_pct"])
        t2_defect_rows.append({
            "doc_id": doc_id,
            "sec_num": sec_num,
            "best_citation": best["citation"],
            "best_p_contradiction_pct": best["p_contradiction_pct"],
            "d_g": best["d_g"],
            "tau_dyn": best["tau_dyn"],
            "hit_static_045": any(r["hit_static_045"] for r in rows),
            "hit_kg_tau": any(r["hit_kg_tau"] for r in rows),
            "hit_kg_plus_numeric": any(r["hit_kg_plus_numeric"] for r in rows),
            "all_pairs": rows,
        })

    # --- Tier 3 V0 (all 10 cases, 100% verbatim PDF section + positive-law corpus provisions) ---
    t3_cases = [json.loads(ln) for ln in open(TIER3_CASES_PATH, encoding="utf-8") if ln.strip()]
    pdf_by_case = dict(TIER3_CASES)
    pdf_cache = {}
    t3_pairs = []
    t3_meta = []

    for c in t3_cases:
        cid = c["case_id"]
        pdf_name = c.get("challenged_pdf_name") or pdf_by_case[cid]
        sec_num = int(c["challenged_sec_num"])
        pdf_path = TIER3_PDF_DIR / pdf_name
        pdf_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:16]
        if pdf_sha not in pdf_cache:
            raw_pdf = "\n\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(str(pdf_path)).pages).strip()
            _, chs = demo_app.chunk_ordinance_sections(raw_pdf, default_title=pdf_name)
            pdf_cache[pdf_sha] = (raw_pdf, demo_app.extract_cited_enactment_ids(raw_pdf), {ch["sec_num"]: ch for ch in chs})
        raw_doc_txt, doc_cited, c_map = pdf_cache[pdf_sha]
        ch = c_map[sec_num]
        s_marker = ch.get("sec_marker") or f"SECTION {sec_num}"
        hdr = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
        hyp = f"[{hdr}] {ch['text']}".strip()

        premise_items = []
        for extra in c.get("extra_premises", []):
            premise_items.append((None, extra["citation"], (extra.get("raw_text") or "").lstrip("- \r\n").strip()))
        for pid in c.get("target_provision_ids", []):
            rec = corpus_kg.records_by_pid[pid]
            cit = f"{rec.get('enactment_number') or rec.get('enactment_id')} {rec.get('section_number') or ''}".strip()
            st_txt = (rec.get("raw_text") or "").lstrip("- \r\n").strip()
            premise_items.append((pid, cit, st_txt))

        for pid, cit, st_txt in premise_items:
            prem = f"[{cit}] {st_txt}".strip()
            t3_pairs.append((prem, hyp))
            t3_meta.append((c, sec_num, ch["text"], doc_cited, pid, cit, st_txt))

    t3_res = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(t3_pairs)
    t3_per_case = defaultdict(list)
    t3_case_meta = {}
    for meta, sc in zip(t3_meta, t3_res):
        c, sec_num, dr_txt, doc_cited, pid, cit, st_txt = meta
        cid = c["case_id"]
        t3_case_meta[cid] = (c, sec_num)
        d_g, dom, rel = demo_app.compute_topological_distance(cit, dr_txt, st_txt, draft_cited_eids=doc_cited)
        tau_dyn = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
        num_chk = demo_app.verify_dynamic_numeric_bounds(st_txt, dr_txt)
        p_c = float(sc["p_contradiction"])
        t3_per_case[cid].append({
            "provision_id": pid,
            "citation": cit,
            "p_contradiction_pct": round(p_c * 100.0, 2),
            "p_entailment_pct": round(float(sc["p_entailment"]) * 100.0, 2),
            "d_g": d_g,
            "relation_type": rel,
            "tau_dyn": tau_dyn,
            "hit_static_045": p_c >= 0.45,
            "hit_kg_tau": p_c >= tau_dyn,
            "numeric_breach": num_chk if num_chk["breached"] else None,
            "hit_kg_plus_numeric": (p_c >= tau_dyn) or bool(num_chk["breached"]),
        })

    t3_rows = []
    for c in t3_cases:
        cid = c["case_id"]
        rows = t3_per_case[cid]
        best = max(rows, key=lambda r: r["p_contradiction_pct"])
        num_hit_row = next((r for r in rows if r["numeric_breach"] is not None), None)
        gold_is_c = (c.get("gold_nli_label") == "Contradiction")
        t3_rows.append({
            "case_id": cid,
            "case_name": c["case_name"],
            "controlling_statute": c["controlling_statute"],
            "challenged_sec_num": t3_case_meta[cid][1],
            "gold_label": c.get("gold_nli_label"),
            "gold_is_conflict": gold_is_c,
            "best_citation": best["citation"],
            "best_p_contradiction_pct": best["p_contradiction_pct"],
            "p_contradiction_pct": best["p_contradiction_pct"],
            "d_g": best["d_g"],
            "relation_type": best["relation_type"],
            "tau_dyn": best["tau_dyn"],
            "pred_static_045": any(r["hit_static_045"] for r in rows),
            "pred_kg_tau": any(r["hit_kg_tau"] for r in rows),
            "numeric_breach": num_hit_row["numeric_breach"] if num_hit_row else None,
            "pred_kg_plus_numeric": any(r["hit_kg_plus_numeric"] for r in rows),
            "all_pairs": rows,
        })

    def binary_acc(rows, pred_key):
        tp = sum(1 for r in rows if r["gold_is_conflict"] and r[pred_key])
        fp = sum(1 for r in rows if not r["gold_is_conflict"] and r[pred_key])
        tn = sum(1 for r in rows if not r["gold_is_conflict"] and not r[pred_key])
        fn = sum(1 for r in rows if r["gold_is_conflict"] and not r[pred_key])
        return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "acc_pct": round((tp + tn) / len(rows) * 100.0, 2)}

    t2_v0_sum = {
        "static_045_hits": sum(1 for r in t2_defect_rows if r["hit_static_045"]),
        "kg_tau_hits": sum(1 for r in t2_defect_rows if r["hit_kg_tau"]),
        "kg_tau_plus_numeric_hits": sum(1 for r in t2_defect_rows if r["hit_kg_plus_numeric"]),
        "total_defects": len(t2_defect_rows),
        "per_defect": t2_defect_rows,
    }
    t3_v0_sum = {
        "static_045": binary_acc(t3_rows, "pred_static_045"),
        "kg_tau": binary_acc(t3_rows, "pred_kg_tau"),
        "kg_tau_plus_numeric": binary_acc(t3_rows, "pred_kg_plus_numeric"),
        "per_case": t3_rows,
    }
    print(f"[V0 Tier 2] Static 0.45={t2_v0_sum['static_045_hits']}/7 | KG tau*={t2_v0_sum['kg_tau_hits']}/7 | +Numeric={t2_v0_sum['kg_tau_plus_numeric_hits']}/7")
    print(f"[V0 Tier 3] Static 0.45={t3_v0_sum['static_045']} | KG tau*={t3_v0_sum['kg_tau']} | +Numeric={t3_v0_sum['kg_tau_plus_numeric']}")
    return {"tier2": t2_v0_sum, "tier3": t3_v0_sum}


def write_tier2_report(doc_results: list, summary: dict):
    bm = summary["binary_metrics"]
    cm = summary["binary_confusion_matrix"]
    tm = summary["three_class_metrics"]
    with open(OUT_TIER2_SYNC_TXT, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("OFFICIAL TIER 2 SYNTHETIC DRAFT AUDIT: FULL-PDF SYNCHRONIZED LOG (DYNAMIC V5)\n")
        f.write("Platform: MiniLM-L6-v2 + BM25 CSR + Tuned DeBERTa-v3 + Real KG tau* + Dynamic Numeric Bounds\n")
        f.write("================================================================================\n\n")
        f.write(f"SUMMARY | Docs: {summary['documents_evaluated']} | Sections: {summary['provisions_evaluated']} | UI Pairs Flagged: {summary['total_ui_conflict_pairs']} | Exact Gold Statute Matches: {summary['exact_answer_key_statute_matches']}/7\n")
        f.write(f"BINARY  | TP={cm['true_positives']} FP={cm['false_positives']} TN={cm['true_negatives']} FN={cm['false_negatives']} | Prec={bm['contradiction_precision']*100:.2f}% | Rec={bm['contradiction_recall']*100:.2f}% | Spec={bm['section_level_specificity_pct']:.2f}% | F1={bm['contradiction_f1']:.4f} | F2={bm['cost_sensitive_f2']:.4f} | BinAcc={bm['binary_screening_accuracy_pct']:.2f}%\n")
        f.write(f"3-CLASS | Acc={tm['three_class_accuracy_pct']:.2f}% ({tm['three_class_correct']}/{summary['provisions_evaluated']}) | Macro-F1={tm['macro_f1']:.4f}\n\n")

        for r in doc_results:
            f.write("#" * 80 + "\n")
            f.write(f"DRAFT: {r['doc_id']} ({r['functional_typology']}) | PDF: {r['pdf_name']} | Pages: {r['pdf_pages']} | Words: {r['total_document_words']}\n")
            f.write(f"Total Sections: {r['total_sections']} ({r['substantive_sections']} op.) | Stage1: {r['latency_metrics'].get('stage1_latency_s')}s | Stage2: {r['latency_metrics'].get('stage2_latency_s')}s | Total: {r['audit_latency_s']}s\n")
            f.write(f"UI Headline: {r['total_conflicts_found']} Conflicts Detected! ({len(r['problematic_sections'])} Problematic Sections: {r['problematic_sections']})\n")
            f.write("#" * 80 + "\n\n")
            for idx, p in enumerate(r["conflict_pairs"], 1):
                f.write(f"--- Conflict #{idx} --------------------------------------------------------\n")
                f.write(f"Draft Provision : Section {p['sec_num']} ({p['sec_title']})\n")
                f.write(f"Target Statute  : {p['target_statute']}\n")
                f.write(f"Confidence      : {p['confidence_pct']}% | tau* = {p['dynamic_threshold_pct']}% (d_G = {p.get('graph_distance_d_g', '?')})\n")
                f.write(f"Top Draft Saliency   : {[(t['token'], t['weight']) for t in p['top_ordinance_xai'][:8]]}\n")
                f.write(f"Top Statute Saliency : {[(t['token'], t['weight']) for t in p['top_statute_xai'][:8]]}\n")
                f.write(f"Legal Rationale : {p['legal_rationale']}\n\n")
            f.write("\n")


def run_tier2_suite(corpus_kg: UnifiedCorpusAndKG, v0_results: dict):
    print("\n" + "=" * 88)
    print("TIER 2 SUITE: FULL STAGE-BY-STAGE ABLATION (V1..V6 ACROSS ALL 6 FOLIO PDFs)")
    print("=" * 88)

    gold_docs = {}
    with open(TIER2_BENCHMARK_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                gold_docs[d["doc_id"]] = d

    pdf_files = sorted(TIER2_PDF_DIR.glob("DRAFT-ORD-2026-*.pdf"))
    pdf_texts = {}
    pdf_meta = {}
    for p in pdf_files:
        reader = pypdf.PdfReader(str(p))
        txt = "\n\n".join(pg.extract_text() or "" for pg in reader.pages).strip()
        pdf_texts[p.stem] = txt
        pdf_meta[p.stem] = {
            "pdf_name": p.name,
            "pdf_pages": len(reader.pages),
            "pdf_sha256_prefix": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
            "total_document_words": len(txt.split()),
        }

    variants_out = {}

    # V5 Full System (runs live execute_full_ordinance_audit -> populates Stage 2 cache + XAI!)
    print("\n--- Running V5_full_system (Hybrid + Real KG tau* + Dynamic Numeric Bounds) ---")
    v5_raw = {}
    v5_docs = []
    v5_provs = []
    v5_lat = 0.0
    for doc_id in sorted(gold_docs.keys()):
        t0 = time.perf_counter()
        data = demo_app.execute_full_ordinance_audit(
            pdf_texts[doc_id], pdf_meta[doc_id]["pdf_name"], doc_id=None,
            retrieval_mode="hybrid", use_kg_threshold=True, use_numeric_bounds=True,
        )
        dt = time.perf_counter() - t0
        v5_lat += dt
        v5_raw[doc_id] = data
        doc_rec, sec_evals = evaluate_tier2_sections_against_gold(doc_id, gold_docs[doc_id], data["sections"], dt)
        doc_rec.update(pdf_meta[doc_id])
        doc_rec["total_sections"] = data.get("total_sections", 0)
        doc_rec["substantive_sections"] = sum(1 for s in data["sections"] if not s.get("is_boilerplate"))
        doc_rec["latency_metrics"] = data.get("latency_metrics", {})
        v5_docs.append(doc_rec)
        v5_provs.extend(sec_evals)
        print(f"  [V5] {doc_id}: {dt:.2f}s | Pairs={doc_rec['total_conflicts_found']} Secs={doc_rec['problematic_sections']} | TP={doc_rec['true_positive_contradictions']}/{doc_rec['gold_contradictions']}")

    v5_sum = compute_tier2_metrics(v5_provs, v5_docs)
    v5_sum["total_audit_latency_s"] = round(v5_lat, 2)
    variants_out["V5_full_system"] = {"summary": v5_sum, "documents": v5_docs}

    # Save synchronized Tier 2 V5 live-demo artifacts
    OUT_TIER2_SYNC_JSON.write_text(json.dumps({
        "benchmark_tier": "Tier 2: Synchronized Live-Demo Full-PDF Audit (Dynamic V5)",
        "summary_metrics": v5_sum,
        "document_level_results": v5_docs,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    write_tier2_report(v5_docs, v5_sum)

    # V3 & V4 derived identically from V5 (same Stage 1 Top-8 & DeBERTa probs)
    for vname, use_kg_t, use_num in (
        ("V3_hybrid_pure_neural_static", False, False),
        ("V4_hybrid_neural_kg_tau", True, False),
    ):
        v_docs, v_provs = [], []
        for doc_id in sorted(gold_docs.keys()):
            der_secs = derive_stage2_variant_sections(v5_raw[doc_id]["sections"], use_kg_t, use_num)
            d_rec, s_ev = evaluate_tier2_sections_against_gold(doc_id, gold_docs[doc_id], der_secs, 0.0)
            v_docs.append(d_rec)
            v_provs.extend(s_ev)
        v_sum = compute_tier2_metrics(v_provs, v_docs)
        variants_out[vname] = {"summary": v_sum, "documents": v_docs}
        print(f"  [{vname}] TP={v_sum['binary_confusion_matrix']['true_positives']} FP={v_sum['binary_confusion_matrix']['false_positives']} Spec={v_sum['binary_metrics']['section_level_specificity_pct']:.2f}% ExactGold={v_sum['exact_answer_key_statute_matches']}/7 UI_Pairs={v_sum['total_ui_conflict_pairs']}")

    # V1 (BM25 only) & V2 (MiniLM dense only)
    for vname, rmode in (("V1_bm25_only", "bm25"), ("V2_minilm_only", "dense")):
        print(f"\n--- Running {vname} (retrieval_mode={rmode}) ---")
        v_docs, v_provs, v_lat = [], [], 0.0
        for doc_id in sorted(gold_docs.keys()):
            t0 = time.perf_counter()
            data = demo_app.execute_full_ordinance_audit(
                pdf_texts[doc_id], pdf_meta[doc_id]["pdf_name"], doc_id=None,
                retrieval_mode=rmode, use_kg_threshold=True, use_numeric_bounds=True,
            )
            dt = time.perf_counter() - t0
            v_lat += dt
            d_rec, s_ev = evaluate_tier2_sections_against_gold(doc_id, gold_docs[doc_id], data["sections"], dt)
            d_rec["latency_metrics"] = data.get("latency_metrics", {})
            v_docs.append(d_rec)
            v_provs.extend(s_ev)
            print(f"  [{vname}] {doc_id}: {dt:.2f}s | Pairs={d_rec['total_conflicts_found']} Secs={d_rec['problematic_sections']} | TP={d_rec['true_positive_contradictions']}/{d_rec['gold_contradictions']}")
        v_sum = compute_tier2_metrics(v_provs, v_docs)
        v_sum["total_audit_latency_s"] = round(v_lat, 2)
        variants_out[vname] = {"summary": v_sum, "documents": v_docs}

    # V6 (Hybrid + Real 1-Hop KG Expansion)
    print("\n--- Running V6_hybrid_kg_expansion ---")
    v6_docs, v6_provs, v6_added_lat = [], [], 0.0
    for doc_id in sorted(gold_docs.keys()):
        aug_secs, ts1, ts2 = run_kg_expansion_on_audit(pdf_texts[doc_id], pdf_meta[doc_id]["pdf_name"], v5_raw[doc_id], corpus_kg)
        v6_added_lat += ts1 + ts2
        d_rec, s_ev = evaluate_tier2_sections_against_gold(doc_id, gold_docs[doc_id], aug_secs, ts1 + ts2)
        v6_docs.append(d_rec)
        v6_provs.extend(s_ev)
        print(f"  [V6] {doc_id}: +S1={ts1}s +S2={ts2}s | Pairs={d_rec['total_conflicts_found']} Secs={d_rec['problematic_sections']} | TP={d_rec['true_positive_contradictions']}/{d_rec['gold_contradictions']}")
    v6_sum = compute_tier2_metrics(v6_provs, v6_docs)
    v6_sum["added_kg_latency_s"] = round(v6_added_lat, 2)
    v6_sum["total_audit_latency_s"] = round(v5_lat + v6_added_lat, 2)
    variants_out["V6_hybrid_kg_expansion"] = {"summary": v6_sum, "documents": v6_docs}

    payload = {"v0_isolated_stage2": v0_results["tier2"], "full_pdf_variants": variants_out}
    OUT_TIER2_ABL.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Saved Tier 2 ablation suite -> {OUT_TIER2_ABL}")
    return payload


def summarize_tier3_case(case_id: str, pdf_name: str, pdf_pages: int, pdf_sha: str, sections: list, latency_s: float, latency_metrics: dict = None) -> dict:
    pairs = extract_conflict_pairs_from_sections(sections)
    distinct_secs = sorted(set(p["sec_num"] for p in pairs))
    substantive = sum(1 for s in sections if not s.get("is_boilerplate"))
    return {
        "case_id": case_id,
        "pdf_name": pdf_name,
        "pdf_pages": pdf_pages,
        "pdf_sha256_prefix": pdf_sha,
        "audit_latency_s": round(latency_s, 2),
        "latency_metrics": latency_metrics or {},
        "total_sections": len(sections),
        "substantive_sections": substantive,
        "total_conflicts_found": len(pairs),
        "problematic_sections": distinct_secs,
        "conflict_pairs": pairs,
    }


def write_tier3_report(results_map: dict):
    with open(OUT_TIER3_SYNC_TXT, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("OFFICIAL TIER 3 SUPREME COURT PREEMPTION AUDIT: FULL-PDF SYNCHRONIZED LOG (DYNAMIC V5)\n")
        f.write("Platform: MiniLM-L6-v2 + BM25 CSR + Tuned DeBERTa-v3 + Real KG tau* + Dynamic Numeric Bounds\n")
        f.write("================================================================================\n\n")
        for cid, _ in TIER3_CASES:
            if cid not in results_map:
                continue
            r = results_map[cid]
            f.write("#" * 80 + "\n")
            f.write(f"CASE: {cid} | Document: {r['pdf_name']} | Pages: {r.get('pdf_pages', '?')}\n")
            f.write(f"Total Sections: {r['total_sections']} ({r.get('substantive_sections', '?')} op.) | Latency: {r['audit_latency_s']}s\n")
            f.write(f"UI Headline: {r['total_conflicts_found']} Conflicts Detected!\n")
            f.write(f"UI Subheadline: {len(r['problematic_sections'])} Problematic Sections: {r['problematic_sections']}\n")
            f.write("#" * 80 + "\n\n")
            if not r["conflict_pairs"]:
                f.write("   [VERDICT] All substantive provisions passed calibrated threshold tau* (0 Conflicts Detected).\n\n")
            else:
                for idx, p in enumerate(r["conflict_pairs"], 1):
                    f.write(f"--- Conflict #{idx} --------------------------------------------------------\n")
                    f.write(f"Draft Provision : Section {p['sec_num']} ({p['sec_title']})\n")
                    f.write(f"Target Statute  : {p['target_statute']}\n")
                    f.write(f"Confidence      : {p['confidence_pct']}% | tau* = {p['dynamic_threshold_pct']}% (d_G = {p.get('graph_distance_d_g', '?')})\n")
                    f.write(f"Top Draft Saliency   : {[(t['token'], t['weight']) for t in p['top_ordinance_xai'][:8]]}\n")
                    f.write(f"Top Statute Saliency : {[(t['token'], t['weight']) for t in p['top_statute_xai'][:8]]}\n")
                    f.write(f"Legal Rationale : {p['legal_rationale']}\n\n")
            f.write("\n")


def run_tier3_std8_suite(corpus_kg: UnifiedCorpusAndKG, v0_results: dict):
    print("\n" + "=" * 88)
    print("TIER 3 STANDARD 8 SUITE: FULL STAGE-BY-STAGE ABLATION (V1..V6)")
    print("=" * 88)

    std8 = [c for c in TIER3_CASES if c[0] not in ("DAVAO-TIER3-03", "DAVAO-TIER3-04")]
    pdf_info = {}
    for cid, pdf_name in std8:
        p = TIER3_PDF_DIR / pdf_name
        reader = pypdf.PdfReader(str(p))
        txt = "\n\n".join(pg.extract_text() or "" for pg in reader.pages).strip()
        pdf_info[cid] = {
            "pdf_name": pdf_name,
            "pages": len(reader.pages),
            "sha": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
            "text": txt,
        }

    variants = defaultdict(dict)
    v5_raw = {}

    print("\n--- Running V5_full_system on Tier 3 Standard 8 ---")
    for cid, _ in std8:
        info = pdf_info[cid]
        t0 = time.perf_counter()
        data = demo_app.execute_full_ordinance_audit(
            info["text"], info["pdf_name"], doc_id=None,
            retrieval_mode="hybrid", use_kg_threshold=True, use_numeric_bounds=True,
        )
        dt = time.perf_counter() - t0
        v5_raw[cid] = data
        variants["V5_full_system"][cid] = summarize_tier3_case(cid, info["pdf_name"], info["pages"], info["sha"], data["sections"], dt, data.get("latency_metrics"))
        print(f"  [V5] {cid}: {dt:.2f}s | UI Pairs={variants['V5_full_system'][cid]['total_conflicts_found']} Secs={variants['V5_full_system'][cid]['problematic_sections']}")

    # Sync Tier 3 JSON & TXT with V5 results (preserving existing RevCode entries until tier3_revcode runs)
    sync_map = {}
    if OUT_TIER3_SYNC_JSON.exists():
        try:
            sync_map = json.loads(OUT_TIER3_SYNC_JSON.read_text(encoding="utf-8"))
        except Exception:
            sync_map = {}
    sync_map.update(variants["V5_full_system"])
    OUT_TIER3_SYNC_JSON.write_text(json.dumps(sync_map, indent=2, ensure_ascii=False), encoding="utf-8")
    write_tier3_report(sync_map)

    # Derive V3 & V4
    for vname, use_kg_t, use_num in (("V3_hybrid_pure_neural_static", False, False), ("V4_hybrid_neural_kg_tau", True, False)):
        for cid, _ in std8:
            info = pdf_info[cid]
            der = derive_stage2_variant_sections(v5_raw[cid]["sections"], use_kg_t, use_num)
            variants[vname][cid] = summarize_tier3_case(cid, info["pdf_name"], info["pages"], info["sha"], der, 0.0)
            print(f"  [{vname}] {cid}: UI Pairs={variants[vname][cid]['total_conflicts_found']} Secs={variants[vname][cid]['problematic_sections']}")

    # Run V1 (BM25 only) & V2 (MiniLM only)
    for vname, rmode in (("V1_bm25_only", "bm25"), ("V2_minilm_only", "dense")):
        print(f"\n--- Running {vname} on Tier 3 Standard 8 ---")
        for cid, _ in std8:
            info = pdf_info[cid]
            t0 = time.perf_counter()
            data = demo_app.execute_full_ordinance_audit(
                info["text"], info["pdf_name"], doc_id=None,
                retrieval_mode=rmode, use_kg_threshold=True, use_numeric_bounds=True,
            )
            dt = time.perf_counter() - t0
            variants[vname][cid] = summarize_tier3_case(cid, info["pdf_name"], info["pages"], info["sha"], data["sections"], dt, data.get("latency_metrics"))
            print(f"  [{vname}] {cid}: {dt:.2f}s | UI Pairs={variants[vname][cid]['total_conflicts_found']} Secs={variants[vname][cid]['problematic_sections']}")

    # Run V6 (1-Hop KG Expansion)
    print("\n--- Running V6_hybrid_kg_expansion on Tier 3 Standard 8 ---")
    for cid, _ in std8:
        info = pdf_info[cid]
        aug_secs, ts1, ts2 = run_kg_expansion_on_audit(info["text"], info["pdf_name"], v5_raw[cid], corpus_kg)
        variants["V6_hybrid_kg_expansion"][cid] = summarize_tier3_case(cid, info["pdf_name"], info["pages"], info["sha"], aug_secs, variants["V5_full_system"][cid]["audit_latency_s"] + ts1 + ts2)
        print(f"  [V6] {cid}: +S1={ts1}s +S2={ts2}s | UI Pairs={variants['V6_hybrid_kg_expansion'][cid]['total_conflicts_found']} Secs={variants['V6_hybrid_kg_expansion'][cid]['problematic_sections']}")

    out_payload = {"v0_isolated_stage2": v0_results["tier3"], "standard8_variants": dict(variants)}
    OUT_TIER3_STD8_ABL.write_text(json.dumps(out_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Saved Tier 3 Standard 8 ablation -> {OUT_TIER3_STD8_ABL}")
    return out_payload


def run_tier3_revcode_suite(corpus_kg: UnifiedCorpusAndKG):
    print("\n" + "=" * 88)
    print("TIER 3 REVENUE CODE SUITE: FULL 423-SECTION V3/V4/V5 + TARGETED V1/V2/V6 (SEC 69 & 423)")
    print("=" * 88)

    p3 = TIER3_PDF_DIR / "03_arc_investors_holding_tax.pdf"
    p4 = TIER3_PDF_DIR / "04_first_meridian_payment_under_protest.pdf"
    sha3 = hashlib.sha256(p3.read_bytes()).hexdigest()[:16]
    sha4 = hashlib.sha256(p4.read_bytes()).hexdigest()[:16]
    reader = pypdf.PdfReader(str(p3))
    raw_text = "\n\n".join(pg.extract_text() or "" for pg in reader.pages).strip()

    last_print = [0.0]

    def cb(stage, progress, badge, msg):
        now = time.perf_counter()
        if now - last_print[0] >= 20.0 or progress in (20, 100):
            print(f"    [{progress:3d}%] {stage}: {badge} - {msg}", flush=True)
            last_print[0] = now

    t0 = time.perf_counter()
    data_v5 = demo_app.execute_full_ordinance_audit(
        raw_text, p3.name, doc_id=None, progress_callback=cb,
        retrieval_mode="hybrid", use_kg_threshold=True, use_numeric_bounds=True,
    )
    dt_v5 = time.perf_counter() - t0
    print(f"[V5 RevCode] Completed 435 secs (423 op.) in {dt_v5:.2f}s (S1={data_v5['latency_metrics']['stage1_latency_s']}s, S2={data_v5['latency_metrics']['stage2_latency_s']}s)", flush=True)

    rev_variants = {}
    rev_variants["V5_full_system"] = summarize_tier3_case("DAVAO-TIER3-03", p3.name, len(reader.pages), sha3, data_v5["sections"], dt_v5, data_v5.get("latency_metrics"))

    for vname, use_kg_t, use_num in (("V3_hybrid_pure_neural_static", False, False), ("V4_hybrid_neural_kg_tau", True, False)):
        der = derive_stage2_variant_sections(data_v5["sections"], use_kg_t, use_num)
        rev_variants[vname] = summarize_tier3_case("DAVAO-TIER3-03", p3.name, len(reader.pages), sha3, der, 0.0)

    # Update synchronized all-10 JSON and TXT
    sync_map = {}
    if OUT_TIER3_SYNC_JSON.exists():
        try:
            sync_map = json.loads(OUT_TIER3_SYNC_JSON.read_text(encoding="utf-8"))
        except Exception:
            sync_map = {}
    r03 = dict(rev_variants["V5_full_system"])
    sync_map["DAVAO-TIER3-03"] = r03
    if sha4 == sha3:
        r04 = dict(r03)
        r04["case_id"] = "DAVAO-TIER3-04"
        r04["pdf_name"] = p4.name
        sync_map["DAVAO-TIER3-04"] = r04
    OUT_TIER3_SYNC_JSON.write_text(json.dumps(sync_map, indent=2, ensure_ascii=False), encoding="utf-8")
    write_tier3_report(sync_map)

    # Targeted Stage 1 ablations (V1 BM25, V2 MiniLM, V6 KG-Exp) on challenged sections 69 & 423
    doc_title, chunks = demo_app.chunk_ordinance_sections(raw_text, default_title=p3.name)
    doc_cited_eids = demo_app.extract_cited_enactment_ids(raw_text)
    challenged = [c for c in chunks if c["sec_num"] in (69, 423)]
    targeted = {}
    for vname, rmode in (("V1_bm25_only", "bm25"), ("V2_minilm_only", "dense")):
        t_sub = time.perf_counter()
        sub_secs = []
        for ch in challenged:
            s_marker = ch.get("sec_marker") or f"SECTION {ch['sec_num']}"
            hdr = f"{s_marker}: {ch['sec_title']}" if ch.get("sec_title") else s_marker
            q_str = f"[{doc_title} | {hdr}] {ch['text']}"
            hyp = f"[{hdr}] {ch['text']}"
            raw_c = demo_app.NEURAL_ENGINE.retrieve_top_k(q_str, k=50, scope="national", retrieval_mode=rmode)
            valid_c = [c for c in raw_c if not is_obsolete_colonial(c.get("enactment_id", ""), c.get("citation", ""))]
            ev_c = valid_c[:8]
            pairs = [(f"[{c['citation']}] {(c.get('raw_text') or c.get('prepended_text', '')).lstrip('- \r\n')}".strip(), hyp) for c in ev_c]
            nli_res = demo_app.NEURAL_ENGINE.evaluate_cross_encoder_batch(pairs) if pairs else []
            for cand, r in zip(ev_c, nli_res):
                c_raw = cand.get("raw_text") or cand.get("prepended_text", "")
                d_g, dom, rel_t = demo_app.compute_topological_distance(cand["citation"], ch["text"], c_raw, draft_cited_eids=doc_cited_eids)
                tau_d = demo_app.compute_dynamic_threshold(d_g, is_vertical=True, tau_base=0.45, delta_tau=0.15)
                num_chk = demo_app.verify_dynamic_numeric_bounds(c_raw, ch["text"])
                has_num = bool(num_chk.get("breached"))
                is_c = (r["p_contradiction"] >= tau_d) or has_num
                cand.update({
                    "stage2_evaluated": True, "p_contradiction": r["p_contradiction"],
                    "p_entailment": r["p_entailment"], "p_neutral": r["p_neutral"],
                    "stage2_confidence": max(round(r["p_contradiction"] * 100, 1), 95.0 if has_num else 0.0),
                    "graph_distance_d_g": d_g, "dynamic_threshold": tau_d,
                    "dynamic_threshold_pct": round(tau_d * 100, 1), "numeric_bound_breach": num_chk if has_num else None,
                    "is_conflict": is_c,
                })
            confs = [c for c in ev_c if c.get("is_conflict")]
            sub_secs.append({
                "sec_num": ch["sec_num"], "sec_title": ch.get("sec_title"), "text": ch["text"], "is_boilerplate": False,
                "verdict": "CONTRADICTION" if confs else "NEUTRAL",
                "target_statute": confs[0]["citation"] if confs else (ev_c[0]["citation"] if ev_c else ""),
                "candidate_shortlist": ev_c,
            })
        targeted[vname] = summarize_tier3_case("DAVAO-REVCODE-69-423", p3.name, 2, sha3, sub_secs, time.perf_counter() - t_sub)
    aug_69_423, ts1, ts2 = run_kg_expansion_on_audit(raw_text, p3.name, data_v5, corpus_kg, only_sec_nums={69, 423})
    targeted["V6_hybrid_kg_expansion"] = summarize_tier3_case("DAVAO-REVCODE-69-423", p3.name, 2, sha3, aug_69_423, ts1 + ts2)

    std8_data = json.loads(OUT_TIER3_STD8_ABL.read_text(encoding="utf-8")) if OUT_TIER3_STD8_ABL.exists() else {}
    full_payload = {
        "v0_isolated_stage2": std8_data.get("v0_isolated_stage2", {}),
        "standard8_variants": std8_data.get("standard8_variants", {}),
        "revcode_full_variants": rev_variants,
        "revcode_challenged_sec69_423_variants": targeted,
    }
    OUT_TIER3_FULL_ABL.write_text(json.dumps(full_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Saved consolidated Tier 3 full ablation -> {OUT_TIER3_FULL_ABL}")
    return full_payload


def run_tier3_sc09_and_v0(corpus_kg: UnifiedCorpusAndKG, v0_results: dict):
    """Re-runs SC-PHIL-09 (Magtajas) across V1..V6 after PD 1869 ingestion and updates Tier 3 artifacts."""
    print("\n" + "=" * 88)
    print("TIER 3 SC-PHIL-09 (MAGTAJAS + PD 1869) & V0 VERBATIM REFRESH (V1..V6)")
    print("=" * 88)

    cid = "SC-PHIL-09"
    pdf_name = "09_magtajas_casino_preemption.pdf"
    p9 = TIER3_PDF_DIR / pdf_name
    reader = pypdf.PdfReader(str(p9))
    raw_txt = "\n\n".join(pg.extract_text() or "" for pg in reader.pages).strip()
    pages = len(reader.pages)
    sha = hashlib.sha256(p9.read_bytes()).hexdigest()[:16]

    sc09_variants = {}
    t0 = time.perf_counter()
    data_v5 = demo_app.execute_full_ordinance_audit(
        raw_txt, pdf_name, doc_id=None,
        retrieval_mode="hybrid", use_kg_threshold=True, use_numeric_bounds=True,
    )
    dt_v5 = time.perf_counter() - t0
    sc09_variants["V5_full_system"] = summarize_tier3_case(cid, pdf_name, pages, sha, data_v5["sections"], dt_v5, data_v5.get("latency_metrics"))
    print(f"  [V5] {cid}: {dt_v5:.2f}s | UI Pairs={sc09_variants['V5_full_system']['total_conflicts_found']} Secs={sc09_variants['V5_full_system']['problematic_sections']}")

    for vname, use_kg_t, use_num in (("V3_hybrid_pure_neural_static", False, False), ("V4_hybrid_neural_kg_tau", True, False)):
        der = derive_stage2_variant_sections(data_v5["sections"], use_kg_t, use_num)
        sc09_variants[vname] = summarize_tier3_case(cid, pdf_name, pages, sha, der, 0.0)
        print(f"  [{vname}] {cid}: UI Pairs={sc09_variants[vname]['total_conflicts_found']} Secs={sc09_variants[vname]['problematic_sections']}")

    for vname, rmode in (("V1_bm25_only", "bm25"), ("V2_minilm_only", "dense")):
        t_s = time.perf_counter()
        d_var = demo_app.execute_full_ordinance_audit(
            raw_txt, pdf_name, doc_id=None,
            retrieval_mode=rmode, use_kg_threshold=True, use_numeric_bounds=True,
        )
        dt_var = time.perf_counter() - t_s
        sc09_variants[vname] = summarize_tier3_case(cid, pdf_name, pages, sha, d_var["sections"], dt_var, d_var.get("latency_metrics"))
        print(f"  [{vname}] {cid}: {dt_var:.2f}s | UI Pairs={sc09_variants[vname]['total_conflicts_found']} Secs={sc09_variants[vname]['problematic_sections']}")

    aug_secs, ts1, ts2 = run_kg_expansion_on_audit(raw_txt, pdf_name, data_v5, corpus_kg)
    sc09_variants["V6_hybrid_kg_expansion"] = summarize_tier3_case(cid, pdf_name, pages, sha, aug_secs, dt_v5 + ts1 + ts2)
    print(f"  [V6] {cid}: +S1={ts1}s +S2={ts2}s | UI Pairs={sc09_variants['V6_hybrid_kg_expansion']['total_conflicts_found']} Secs={sc09_variants['V6_hybrid_kg_expansion']['problematic_sections']}")

    if OUT_TIER3_STD8_ABL.exists():
        std8_payload = json.loads(OUT_TIER3_STD8_ABL.read_text(encoding="utf-8"))
        std8_payload["v0_isolated_stage2"] = v0_results["tier3"]
        for vname, vobj in sc09_variants.items():
            std8_payload.setdefault("standard8_variants", {}).setdefault(vname, {})[cid] = vobj
        OUT_TIER3_STD8_ABL.write_text(json.dumps(std8_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] Updated {OUT_TIER3_STD8_ABL}")

    if OUT_TIER3_FULL_ABL.exists():
        full_payload = json.loads(OUT_TIER3_FULL_ABL.read_text(encoding="utf-8"))
        full_payload["v0_isolated_stage2"] = v0_results["tier3"]
        for vname, vobj in sc09_variants.items():
            full_payload.setdefault("standard8_variants", {}).setdefault(vname, {})[cid] = vobj
        OUT_TIER3_FULL_ABL.write_text(json.dumps(full_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] Updated {OUT_TIER3_FULL_ABL}")

    if OUT_TIER3_SYNC_JSON.exists():
        sync_map = json.loads(OUT_TIER3_SYNC_JSON.read_text(encoding="utf-8"))
        sync_map[cid] = sc09_variants["V5_full_system"]
        OUT_TIER3_SYNC_JSON.write_text(json.dumps(sync_map, indent=2, ensure_ascii=False), encoding="utf-8")
        write_tier3_report(sync_map)
        print(f"[OK] Updated {OUT_TIER3_SYNC_JSON} & {OUT_TIER3_SYNC_TXT}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["tier2", "tier3_std8", "tier3_revcode", "tier3_sc09_and_v0", "all"], default="tier2")
    args = parser.parse_args()

    if not demo_app.NEURAL_ENGINE.is_loaded:
        raise RuntimeError("LocalNeuralEngine failed to load!")

    corpus_kg = UnifiedCorpusAndKG()
    v0_results = run_v0_isolated_ablation(corpus_kg)

    if args.suite in ("tier2", "all"):
        run_tier2_suite(corpus_kg, v0_results)
    if args.suite in ("tier3_std8", "all"):
        run_tier3_std8_suite(corpus_kg, v0_results)
    if args.suite in ("tier3_revcode", "all"):
        run_tier3_revcode_suite(corpus_kg)
    if args.suite == "tier3_sc09_and_v0":
        run_tier3_sc09_and_v0(corpus_kg, v0_results)


if __name__ == "__main__":
    main()
