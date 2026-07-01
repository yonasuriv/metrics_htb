from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIR = Path.home() / ".config" / "htb-ctrl" / "cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
CACHE_FILE = CONFIG_DIR / "cache.json"

USER_CONFIG = Path.home() / ".config" / "htb-ctrl" / "config.yml"
REPO_CONFIG = REPO_ROOT / "htb-ctrl.yml"

DEFAULT_CLI_CONFIG = "htb-cli.yml"
DEFAULT_METRICS_CONFIG = "htb-metrics.yml"
