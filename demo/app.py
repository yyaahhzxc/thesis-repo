"""
demo/app.py
===========
Forwarding launcher for src/demo/app.py.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Forward directly to run_demo launcher logic
import run_demo
