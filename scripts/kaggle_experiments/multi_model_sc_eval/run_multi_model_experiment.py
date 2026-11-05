"""
run_multi_model_experiment.py
==============================
Kaggle Cloud GPU Dispatcher for Multi-Model Supreme Court Benchmark Evaluation (Tier 3).

Dispatched via Kaggle API:
  python -m kaggle kernels push -p kaggle_experiments/multi_model_sc_eval

This runner:
1. Verifies cloud GPU availability (Tesla T4/P100).
2. Clones / synchronizes the thesis-repo.
3. Installs execution dependencies.
4. Executes scripts/evaluate_multi_model_sc.py across 5 representative architectures.
5. Exports all comparison artifacts to /kaggle/working/multi_model_artifacts/ for harvesting.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("=" * 80)
    print(" ⚖️  STAGE 2 MULTI-MODEL SUPREME COURT BENCHMARK - KAGGLE CLOUD GPU EXECUTION")
    print("=" * 80)

    # 1. Environment & GPU Audit
    print("\n[+] Step 1: Auditing Cloud Compute Environment...")
    try:
        import torch
        print(f"    PyTorch Version: {torch.__version__}")
        print(f"    CUDA Available:  {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"    GPU Device:      {torch.cuda.get_device_name(0)}")
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"    Total VRAM:      {vram_gb:.2f} GB")
        else:
            print("    ⚠️ CUDA not detected, running on CPU.")
    except ImportError:
        print("    ⚠️ PyTorch not installed in base environment.")

    # 2. Workspace & Repo Synchronization
    print("\n[+] Step 2: Synchronizing Repository Workspace...")
    working_dir = Path("/kaggle/working")
    repo_dir = Path("/tmp/thesis-repo")

    repo_url = "https://github.com/yyaahhzxc/thesis-repo.git"
    if not repo_dir.exists():
        print(f"    Cloning {repo_url} into {repo_dir}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, str(repo_dir)], check=True)
    else:
        print(f"    Pulling latest commits in {repo_dir}...")
        subprocess.run(["git", "-C", str(repo_dir), "pull"], check=True)

    # 3. Dependency Verification
    print("\n[+] Step 3: Verifying Execution Dependencies...")
    required_packages = ["transformers", "sentence-transformers", "rank-bm25", "scikit-learn", "pandas", "numpy"]
    subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + required_packages, check=True)

    # 4. Execute Benchmark Script
    print("\n[+] Step 4: Executing Multi-Model Supreme Court Benchmark...")
    script_eval = repo_dir / "scripts" / "evaluate_multi_model_sc.py"
    subprocess.run([sys.executable, str(script_eval)], cwd=str(repo_dir), check=True)

    # 5. Export Output Artifacts
    print("\n[+] Step 5: Exporting Output Artifacts to /kaggle/working/...")
    export_dest = working_dir / "multi_model_artifacts"
    export_dest.mkdir(parents=True, exist_ok=True)

    repo_output = repo_dir / "output"
    if repo_output.exists():
        for item in repo_output.glob("multi_model_sc_*.*"):
            shutil.copy2(item, export_dest / item.name)
            print(f"    Harvested artifact: {item.name}")

    print("\n" + "=" * 80)
    print(" ✅ MULTI-MODEL KAGGLE GPU BENCHMARK COMPLETED SUCCESSFULLY")
    print(" All artifacts staged in /kaggle/working/multi_model_artifacts/")
    print("=" * 80)

if __name__ == "__main__":
    main()
