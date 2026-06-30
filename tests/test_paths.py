from htb_metrics.paths import REPO_ROOT, HTML_TEMPLATES_DIR, SVG_TEMPLATES_DIR


def test_repo_root_contains_assets_and_generate():
    assert (REPO_ROOT / "generate.py").is_file()
    assert (REPO_ROOT / "assets" / "templates").is_dir()


def test_template_dirs_exist():
    assert HTML_TEMPLATES_DIR.is_dir()
    assert SVG_TEMPLATES_DIR.is_dir()
    assert (HTML_TEMPLATES_DIR / "classic.html").is_file()
