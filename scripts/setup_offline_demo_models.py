"""
scripts/setup_offline_demo_models.py
====================================
Turnkey Offline Model Downloader and Local Engine Setup for
Ex-Ante Davao City Ordinance Conflict Detection.

Downloads and pre-caches the official Stage 1 and Stage 2 models locally into `models/`:
- Stage 1: sentence-transformers/all-MiniLM-L6-v2 (~80 MB)
- Stage 2: cross-encoder/nli-deberta-v3-base (~350 MB)

Also pre-vectorizes the primary statutory candidate premise pool into a local embedding
matrix so that `demo/app.py` executes 100% genuine local neural inference offline
without needing internet access or remote servers.

Usage:
  python scripts/setup_offline_demo_models.py
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Ensure UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_ROOT / "models"
MINILM_DIR = MODELS_DIR / "all-MiniLM-L6-v2"
DEBERTA_DIR = MODELS_DIR / "nli-deberta-v3-base"
OUTPUT_DIR = REPO_ROOT / "output"
LOCAL_EMB_FILE = OUTPUT_DIR / "demo_local_statutory_embeddings.npy"
LOCAL_META_FILE = OUTPUT_DIR / "demo_local_statutory_meta.json"

REQUIRED_PACKAGES = ["torch", "transformers", "sentence_transformers", "rank_bm25"]


def check_and_install_dependencies():
    """Checks and automatically installs torch, transformers, and sentence-transformers if missing."""
    print("=" * 70)
    print(" [Step 1/3] Checking Local Python Environment & Dependencies...")
    print("=" * 70)

    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            if pkg == "sentence_transformers":
                import sentence_transformers
            elif pkg == "rank_bm25":
                import rank_bm25
            else:
                __import__(pkg)
            print(f"  [x] {pkg} is installed.")
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\n  [!] Missing packages: {missing}")
        print("  Installing via pip (this may take a couple minutes on first run)...")
        cmd = [sys.executable, "-m", "pip", "install", *missing]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print("  [ERROR] Pip install failed. Please run manually: pip install " + " ".join(missing))
            sys.exit(1)
        print("  [x] All packages installed successfully!\n")
    else:
        print("  [x] All required dependencies already present.\n")


def download_and_save_models():
    """Downloads models from HuggingFace Hub and saves them to local disk for offline execution."""
    print("=" * 70)
    print(" [Step 2/3] Downloading & Saving Local Neural Models into models/...")
    print("=" * 70)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Stage 1: all-MiniLM-L6-v2
    print(f"\n--- Stage 1 Bi-Encoder: all-MiniLM-L6-v2 ---")
    if MINILM_DIR.exists() and (MINILM_DIR / "model.safetensors").exists():
        print(f"  [x] Model already downloaded locally at: {MINILM_DIR}")
    else:
        print(f"  Downloading sentence-transformers/all-MiniLM-L6-v2 (~80 MB)...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        model.save(str(MINILM_DIR))
        print(f"  [x] Saved all-MiniLM-L6-v2 to: {MINILM_DIR}")

    # 2. Stage 2: cross-encoder/nli-deberta-v3-base
    print(f"\n--- Stage 2 Cross-Encoder: nli-deberta-v3-base ---")
    if DEBERTA_DIR.exists() and any(DEBERTA_DIR.glob("*.safetensors")) or (DEBERTA_DIR / "pytorch_model.bin").exists():
        print(f"  [x] Model already downloaded locally at: {DEBERTA_DIR}")
    else:
        print(f"  Downloading cross-encoder/nli-deberta-v3-base (~350 MB)...")
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        model_id = "cross-encoder/nli-deberta-v3-base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSequenceClassification.from_pretrained(model_id)
        tokenizer.save_pretrained(str(DEBERTA_DIR))
        model.save_pretrained(str(DEBERTA_DIR))
        print(f"  [x] Saved nli-deberta-v3-base to: {DEBERTA_DIR}")


def build_local_statutory_embedding_index():
    """
    Pre-vectorizes primary statutory premises into a local .npy matrix
    so Stage 1 retrieval runs instantaneously offline on the local machine.
    """
    print("\n" + "=" * 70)
    print(" [Step 3/3] Pre-Computing Local Statutory Embedding Index...")
    print("=" * 70)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    from sentence_transformers import SentenceTransformer
    import numpy as np

    print(f"  Loading local MiniLM model from {MINILM_DIR}...")
    embedder = SentenceTransformer(str(MINILM_DIR))

    # Collect statutory premises from canonical cases and benchmark datasets
    statutes = []
    seen = set()

    # 1. Tier 3 Landmark Supreme Court statutes
    tier3_path = REPO_ROOT / "data" / "tier3_jurisprudential_cases.jsonl"
    if tier3_path.exists():
        with open(tier3_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    cit = item.get("controlling_statute", "")
                    if cit and cit not in seen:
                        seen.add(cit)
                        statutes.append({
                            "citation": cit,
                            "title": item.get("statute_title", cit),
                            "text": item.get("premise_text", ""),
                            "jurisdiction": "national"
                        })

    # 2. General statutory provisions pool
    premises_path = REPO_ROOT / "data" / "corpus_statute_premises.json"
    if premises_path.exists():
        try:
            with open(premises_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    cit = item.get("citation", item.get("statute_number", ""))
                    if cit and cit not in seen:
                        seen.add(cit)
                        statutes.append({
                            "citation": cit,
                            "title": item.get("statute_title", cit),
                            "text": item.get("text", item.get("operative_text", "")),
                            "jurisdiction": item.get("jurisdiction", "national")
                        })
        except Exception:
            pass

    # Ensure baseline statutory anchors
    anchors = [
        ("Presidential Decree No. 1144 §6", "Fertilizer and Pesticide Authority exclusive jurisdiction over agricultural chemicals and aerial application.", "national"),
        ("Republic Act No. 7160 §16", "General Welfare Clause authorizing local government units to protect public health and safety.", "national"),
        ("Republic Act No. 7160 §458", "Powers, duties, and functions of the Sangguniang Panlungsod to regulate billboards and signage setbacks.", "national"),
        ("Republic Act No. 7160 §143(f)", "Tax on business for banks and non-bank financial intermediaries authorized by Bangko Sentral ng Pilipinas.", "national"),
        ("Republic Act No. 7160 §193", "Withdrawal of tax exemption privileges of government-owned corporations under the Local Government Code.", "national"),
        ("Republic Act No. 7160 §195", "Protest of assessment without being required to pay under protest for local business taxes.", "national"),
        ("Republic Act No. 7160 §234", "Exemptions from real property taxes under the Local Government Code.", "national"),
        ("Presidential Decree No. 1869 §1", "PAGCOR franchise and regulatory mandate to operate gambling and casinos throughout the Philippines.", "national"),
        ("1987 Constitution, Art. III §1", "Due process of law and equal protection clause protecting legitimate commercial enterprises from arbitrary closure.", "national"),
        ("Executive Order No. 205 §2", "National Telecommunications Commission exclusive jurisdiction over cable television systems and subscriber rates.", "national"),
        ("Republic Act No. 4136 §35", "Land Transportation and Traffic Code classification of highways and speed restrictions.", "national"),
        ("Republic Act No. 7581 §7", "The Price Act reserving unilateral price ceiling mandates exclusively to the President of the Philippines.", "national"),
        ("Republic Act No. 10173 §16", "Data Privacy Act rights of the data subject against permanent storage without consent.", "national"),
        ("Republic Act No. 10863 §200", "Customs Modernization and Tariff Act exclusive jurisdiction of Bureau of Customs at Port of Davao.", "national"),
        ("Republic Act No. 7942 §27", "Philippine Mining Act of 1995 Regalian Doctrine reserving mineral concessions to national government.", "national"),
        ("Republic Act No. 7925 §5", "Public Telecommunications Policy Act vesting telecom licensing exclusively in Congress and NTC.", "national"),
        ("Davao City Ordinance No. 0367-12 §5", "Anti-Smoking Ordinance requiring 10-meter open space buffer from building entrances.", "local"),
        ("Davao City Ordinance No. 0270-23 §4", "Comprehensive Speed Limit Ordinance road classifications for Davao City.", "local"),
        ("Davao City Ordinance No. 092-2000 §7", "Outdoor Advertising and Billboard Regulation in Davao City.", "local")
    ]

    for cit, text, juris in anchors:
        if cit not in seen:
            seen.add(cit)
            statutes.append({
                "citation": cit,
                "title": f"Statutory Authority: {cit}",
                "text": text,
                "jurisdiction": juris
            })

    print(f"  Encoding {len(statutes)} statutory premise anchors with MiniLM...")
    texts = [f"{s['citation']}: {s['title']} | {s['text']}" for s in statutes]
    vectors = embedder.encode(texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True)

    np.save(str(LOCAL_EMB_FILE), vectors)
    with open(LOCAL_META_FILE, "w", encoding="utf-8") as f:
        json.dump(statutes, f, indent=2)

    print(f"  [x] Saved {vectors.shape[0]} embeddings to: {LOCAL_EMB_FILE}")
    print(f"  [x] Saved statutory metadata to: {LOCAL_META_FILE}")
    print("\n" + "=" * 70)
    print(" [COMPLETE] Local Offline AI Engine is Ready!")
    print(" You can now run 'python demo/app.py' and it will execute live neural inference locally.")
    print("=" * 70)


if __name__ == "__main__":
    check_and_install_dependencies()
    download_and_save_models()
    build_local_statutory_embedding_index()
