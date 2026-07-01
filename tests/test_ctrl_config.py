from ctrl_config.loader import load_settings
from ctrl_config.version import project_version


def test_project_version_matches_pyproject():
    import tomllib
    from pathlib import Path

    repo = Path(__file__).resolve().parents[1]
    with (repo / "pyproject.toml").open("rb") as fp:
        expected = tomllib.load(fp)["project"]["version"]
    assert project_version() == expected


def test_cli_flag_beats_yaml(tmp_path, monkeypatch):
    cfg = tmp_path / "htb-ctrl.yml"
    cfg.write_text("auth:\n  api_token: from-yaml\n")
    monkeypatch.chdir(tmp_path)
    s = load_settings(cli_api_token="from-cli", config_paths=[cfg])
    assert s.auth_token == "from-cli"


def test_hide_banner_from_unified_config(tmp_path, monkeypatch):
    cfg = tmp_path / "htb-ctrl.yml"
    cfg.write_text("cli:\n  hide_banner: true\n")
    monkeypatch.chdir(tmp_path)
    s = load_settings(config_paths=[cfg])
    assert s.hide_banner is True
