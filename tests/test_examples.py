from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_examples_layout():
    assert (REPO_ROOT / "examples" / "README.md").is_file()
    assert (REPO_ROOT / "examples" / "config" / ".env.example").is_file()
    assert (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-consumer.yml").is_file()
    assert (REPO_ROOT / "examples" / "workflows" / "htb-metrics-fork.yml").is_file()
    assert (REPO_ROOT / "examples" / "badges").is_dir()


def test_badge_previews_exist():
    badges = REPO_ROOT / "examples" / "badges"
    assert any(badges.glob("htb-metrics.classic.png"))
    assert any(badges.glob("htb-metrics.*.png"))


def test_docs_guides_exist():
    guides = REPO_ROOT / "docs" / "guides"
    for name in (
        "getting-started.md",
        "configuration.md",
        "development.md",
        "github-actions.md",
        "templates.md",
        "data-sources.md",
        "troubleshooting.md",
    ):
        assert (guides / name).is_file(), f"missing docs/guides/{name}"


def test_config_examples_reference_docs():
    env_example = (REPO_ROOT / "examples" / "config" / ".env.example").read_text()
    yaml_example = (REPO_ROOT / "examples" / "config" / "htb-metrics.yml.example").read_text()
    assert "docs/guides" in env_example
    assert "examples/config" in yaml_example
