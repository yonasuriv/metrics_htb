import json
from pathlib import Path

import pytest

from ctrl_cli.config import bootstrap_cli_config, resolve_auth_token


def test_resolve_auth_token_cli_overrides_env(monkeypatch):
    monkeypatch.setenv("HTB_TOKEN", "env-token")
    assert resolve_auth_token(cli_api_token="cli-token") == "cli-token"


def test_resolve_auth_token_from_env_mode(monkeypatch):
    monkeypatch.setenv("HTB_BEARER", "env-bearer")
    assert resolve_auth_token(cli_bearer="cli-bearer", from_env=True) == "env-bearer"


def test_resolve_auth_token_reads_metrics_yaml(tmp_path):
    metrics = tmp_path / "htb-metrics.yml"
    metrics.write_text("token: metrics-token\n")
    assert resolve_auth_token(metrics_config=str(metrics)) == "metrics-token"


def test_resolve_auth_token_reads_cli_yaml_before_metrics(tmp_path):
    cli = tmp_path / "htb-cli.yml"
    metrics = tmp_path / "htb-metrics.yml"
    cli.write_text("token: cli-token\n")
    metrics.write_text("token: metrics-token\n")
    assert resolve_auth_token(cli_config=str(cli), metrics_config=str(metrics)) == "cli-token"


def test_resolve_auth_token_reads_saved_json(tmp_path, monkeypatch):
    config_dir = tmp_path / ".config" / "htb-ctrl" / "cli"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    config_file.write_text(json.dumps({"token": "saved-token"}))
    monkeypatch.setattr("ctrl_cli.config.CONFIG_FILE", config_file)
    assert resolve_auth_token() == "saved-token"


def test_bootstrap_cli_config_from_env(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("HTB_API_TOKEN=env-api\n")
    token = bootstrap_cli_config(from_env=True)
    assert token == "env-api"


def test_bootstrap_from_env_requires_dotenv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="examples/config/.env.example"):
        bootstrap_cli_config(from_env=True)
