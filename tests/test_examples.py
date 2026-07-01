from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_examples_layout():
    assert (REPO_ROOT / "examples" / "README.md").is_file()
    assert (REPO_ROOT / "examples" / "config" / ".env.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-cli.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "sheets" / "htb_machines_example.xlsx").is_file()
    assert (REPO_ROOT / "examples" / "sheets" / "htb_machines_template.xlsx").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-consumer.yml").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-fork.yml").is_file()
    assert (REPO_ROOT / "examples" / "badges").is_dir()


def test_badge_previews_exist():
    badges = REPO_ROOT / "examples" / "badges"
    assert any(badges.glob("htb-metrics.classic.png"))
    assert any(badges.glob("htb-metrics.*.png"))


def test_docs_guides_exist():
    for section, names in {
        "badge": (
            "getting-started.md",
            "configuration.md",
            "development.md",
            "github-actions.md",
            "templates.md",
            "data-sources.md",
            "troubleshooting.md",
        ),
        "cli": (
            "getting-started.md",
            "usage.md",
            "configuration.md",
            "development.md",
            "troubleshooting.md",
        ),
        "dashboard": (
            "getting-started.md",
            "features.md",
            "customization.md",
            "development.md",
        ),
    }.items():
        guides = REPO_ROOT / "docs" / "guides" / section
        for name in names:
            assert (guides / name).is_file(), f"missing docs/guides/{section}/{name}"


def test_htbctrl_entry_point_exists():
    assert (REPO_ROOT / "htbctrl.py").is_file()


def test_config_examples_reference_docs():
    env_example = (REPO_ROOT / "examples" / "config" / ".env.example").read_text()
    yaml_example = (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").read_text()
    cli_yaml = (REPO_ROOT / "examples" / "config" / "htb-cli.yml.example").read_text()
    assert "docs/guides" in env_example
    assert "examples/config" in yaml_example
    assert "docs/guides/cli" in cli_yaml


def test_dashboard_docs_reference_example_sheet():
    getting_started = (REPO_ROOT / "docs" / "guides" / "dashboard" / "getting-started.md").read_text()
    assert "examples/sheets/htb_machines_example.xlsx" in getting_started
    assert "htb_machines.xlsx" in getting_started
    assert "htb_machines_UPDATE.xlsx" not in getting_started
