from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
BADGE_ASSETS = REPO_ROOT / ".github" / "assets" / "badges"


def test_examples_layout():
    assert (REPO_ROOT / "examples" / "README.md").is_file()
    assert (REPO_ROOT / "examples" / "config" / ".env.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-cli.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-ctrl.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-consumer.yml").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-fork.yml").is_file()
    assert BADGE_ASSETS.is_dir()


def test_badge_previews_exist():
    assert any(BADGE_ASSETS.glob("htb-metrics.*.svg"))
    assert any(BADGE_ASSETS.glob("htb-metrics.github-metrics.classic.svg"))


def test_docs_guides_exist():
    guides = REPO_ROOT / "docs" / "guides"
    expected = (
        "README.md",
        "installation.md",
        "configuration.md",
        "cli-getting-started.md",
        "cli-usage.md",
        "cli-development.md",
        "cli-troubleshooting.md",
        "badge-getting-started.md",
        "badge-github-actions.md",
        "badge-templates.md",
        "badge-data-sources.md",
        "badge-development.md",
        "badge-troubleshooting.md",
        "dashboard-getting-started.md",
        "dashboard-features.md",
        "dashboard-customization.md",
        "dashboard-development.md",
    )
    for name in expected:
        assert (guides / name).is_file(), f"missing docs/guides/{name}"

    for subdir in ("cli", "badge", "dashboard"):
        assert not (guides / subdir).exists(), f"docs/guides/{subdir}/ should be flattened"


def test_htbctrl_entry_point_exists():
    assert (REPO_ROOT / "htbctrl.py").is_file()
    assert (REPO_ROOT / "scripts" / "install.sh").is_file()


def test_config_examples_reference_docs():
    env_example = (REPO_ROOT / "examples" / "config" / ".env.example").read_text()
    yaml_example = (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").read_text()
    cli_yaml = (REPO_ROOT / "examples" / "config" / "htb-cli.yml.example").read_text()
    unified = (REPO_ROOT / "examples" / "config" / "htb-ctrl.yml.example").read_text()
    assert "docs/guides" in env_example
    assert "examples/config" in yaml_example
    assert "docs/guides" in cli_yaml
    assert "hide_banner" in unified


def test_dashboard_docs_reference_example_sheet():
    getting_started = (REPO_ROOT / "docs" / "guides" / "dashboard-getting-started.md").read_text()
    assert "htb_machines.xlsx" in getting_started
    assert "htb_machines_UPDATE.xlsx" not in getting_started
