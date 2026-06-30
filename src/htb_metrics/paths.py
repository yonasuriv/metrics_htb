from pathlib import Path

# src/htb_metrics/paths.py → repo root is two levels up
REPO_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = REPO_ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
HTML_TEMPLATES_DIR = TEMPLATES_DIR / "html"
SVG_TEMPLATES_DIR = TEMPLATES_DIR / "svg"
