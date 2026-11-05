"""
Wrapper forwarding execution to scripts/presentation/sync_slides_viewer.py.
"""
import subprocess
import sys
from pathlib import Path

target = Path(__file__).resolve().parent / "presentation" / "sync_slides_viewer.py"
sys.exit(subprocess.run([sys.executable, str(target)] + sys.argv[1:]).returncode)
