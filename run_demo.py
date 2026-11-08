"""
run_demo.py
===========
Convenience launcher for the Ex-Ante Prototype Demo Site.
Starts the Flask server from src/demo/app.py on http://127.0.0.1:5000.

Usage:
    python run_demo.py
    python src/demo/app.py
"""

import sys
import subprocess
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Auto-detect virtual environment with PyTorch if current environment lacks it
try:
    import torch
except ImportError:
    candidates = [
        REPO_ROOT / ".venv" / "Scripts" / "python.exe",
        REPO_ROOT / "venv" / "Scripts" / "python.exe",
        Path("D:/Documents/davao_ocr_thesis/venv/Scripts/python.exe"),
        Path.home() / "Documents" / "davao_ocr_thesis" / "venv" / "Scripts" / "python.exe",
    ]
    venv_python = next((p for p in candidates if p.exists()), None)
    if venv_python and Path(sys.executable).resolve() != venv_python.resolve():
        print(f"[*] PyTorch not found in current interpreter: {sys.executable}")
        print(f"[*] Automatically switching to thesis virtual environment: {venv_python}\n")
        result = subprocess.run([str(venv_python)] + sys.argv)
        sys.exit(result.returncode)
    else:
        print("\n[!] ERROR: PyTorch ('torch') is not installed in the current Python environment.")
        print("[!] Please activate your virtual environment before running:")
        print("    PowerShell: .\\.venv\\Scripts\\Activate.ps1")
        print("    Direct run: .\\.venv\\Scripts\\python.exe run_demo.py\n")
        sys.exit(1)

from src.demo.app import app

if __name__ == "__main__":
    print("[*] Launching Ex-Ante Semantic Conflict Detection System Prototype...")
    print("[*] Local URL: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
