"""
run_stage2_experiment.py
========================
Kaggle Cloud GPU Execution Script for Stage 2 Cross-Encoder NLI Candidate Screening & Ablation.

Automatically dispatched via Kaggle API:
  kaggle kernels push -p kaggle_experiments/stage2_nli

This script:
1. Verifies cloud GPU availability (NVIDIA Tesla T4/P100).
2. Clones or pulls the latest thesis-repo branch.
3. Executes the full Stage 2 model screening benchmark.
4. Generates loss curve visualizations and evaluation metrics.
5. Exports all output artifacts to /kaggle/working/ for automatic retrieval.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("=" * 80)
    print(" ⚖️  STAGE 2 CROSS-ENCODER NLI BENCHMARK - KAGGLE CLOUD GPU EXECUTION")
    print("=" * 80)

    # 1. Environment & GPU Audit
    print("\n[+] Step 1: Auditing Cloud Compute Environment...")
    try:
        import torch
        print(f"    PyTorch Version: {torch.__version__}")
        print(f"    CUDA Available:  {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"    GPU Device:      {torch.cuda.get_device_name(0)}")
            print(f"    Device Count:    {torch.cuda.device_count()}")
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"    Total VRAM:      {vram_gb:.2f} GB")
        else:
            print("    ⚠️ WARNING: CUDA not detected, falling back to CPU.")
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
    required_packages = ["transformers", "rank-bm25", "scikit-learn", "scipy", "pandas", "numpy", "matplotlib"]
    subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + required_packages, check=True)

    # 4. Execute Stage 2 Model Screening Benchmark
    print("\n[+] Step 4: Executing Stage 2 Screening Benchmark...")
    script_screening = repo_dir / "scripts" / "stage2_model_screening.py"
    subprocess.run([sys.executable, str(script_screening), "--mode", "both"], cwd=str(repo_dir), check=True)

    # 5. Generate Visual Assets (Loss Curves)
    print("\n[+] Step 5: Generating Loss Dynamics Visualizations...")
    script_loss = repo_dir / "scripts" / "generate_loss_curves_plot.py"
    if script_loss.exists():
        subprocess.run([sys.executable, str(script_loss)], cwd=str(repo_dir), check=True)

    # 6. Artifact Harvesting & Export
    print("\n[+] Step 6: Exporting Output Artifacts to /kaggle/working/...")
    export_dest = working_dir / "stage2_artifacts"
    export_dest.mkdir(parents=True, exist_ok=True)

    repo_output = repo_dir / "output"
    if repo_output.exists():
        for item in repo_output.glob("*.*"):
            shutil.copy2(item, export_dest / item.name)
            print(f"    Harvested artifact: {item.name}")

    # Also check visualizations
    viz_output = repo_dir / "output" / "visualizations"
    if viz_output.exists():
        viz_dest = export_dest / "visualizations"
        viz_dest.mkdir(parents=True, exist_ok=True)
        for item in viz_output.glob("*.*"):
            shutil.copy2(item, viz_dest / item.name)
            print(f"    Harvested visual artifact: {item.name}")

    print("\n" + "=" * 80)
    print(" ✅ STAGE 2 KAGGLE GPU BENCHMARK COMPLETED SUCCESSFULLY")
    print(" All artifacts staged in /kaggle/working/ for download via 'kaggle kernels output'")
    print("=" * 80)

if __name__ == "__main__":
    main()
