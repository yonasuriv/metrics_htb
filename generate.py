"""Entry point for HTB Metrics (run from repository root)."""
from __future__ import annotations

import sys
from pathlib import Path

_src = Path(__file__).resolve().parent / "src"
if _src.is_dir() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from htb_metrics.cli import main

if __name__ == "__main__":
    main()
