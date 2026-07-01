from ctrl_metrics.paths import (
    REPO_ROOT,
    HTML_TEMPLATES_DIR,
    SVG_TEMPLATES_DIR,
    user_data_dir,
    user_badges_dir,
)


def test_repo_root_contains_assets_and_htbctrl():
    assert (REPO_ROOT / "htbctrl.py").is_file()
    assert (REPO_ROOT / "assets" / "templates").is_dir()


def test_user_paths():
    assert user_data_dir(780424) == REPO_ROOT / "user" / "780424" / "data"
    assert user_badges_dir(780424) == REPO_ROOT / "user" / "780424" / "badges"


def test_template_dirs_exist():
    assert HTML_TEMPLATES_DIR.is_dir()
    assert SVG_TEMPLATES_DIR.is_dir()
    assert (HTML_TEMPLATES_DIR / "classic.html").is_file()
