from pathlib import Path

# src/htb_metrics/paths.py → repo root is two levels up
REPO_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = REPO_ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
HTML_TEMPLATES_DIR = TEMPLATES_DIR / "html"
SVG_TEMPLATES_DIR = TEMPLATES_DIR / "svg"


def user_root(profile_id: int | str) -> Path:
    return REPO_ROOT / "user" / str(profile_id)


def user_data_dir(profile_id: int | str) -> Path:
    return user_root(profile_id) / "data"


def user_badges_dir(profile_id: int | str) -> Path:
    return user_root(profile_id) / "badges"


def default_cache_dir(profile_id: int | str) -> str:
    return user_data_dir(profile_id).relative_to(REPO_ROOT).as_posix()


def default_output_dir(profile_id: int | str) -> str:
    return user_badges_dir(profile_id).relative_to(REPO_ROOT).as_posix()
