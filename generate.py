"""Backward-compatible entry point. Prefer: python htbm.py metrics --generate"""
from __future__ import annotations

import sys

if __name__ == "__main__":
    from htbm import main

    main(["metrics", "--generate", *sys.argv[1:]])
