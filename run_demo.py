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
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.demo.app import app

if __name__ == "__main__":
    print("[*] Launching Ex-Ante Semantic Conflict Detection System Prototype...")
    print("[*] Local URL: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

