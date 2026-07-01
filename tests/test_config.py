import pytest
import os
from ctrl_metrics.config import load_config, Config, resolve_auth_token

def test_load_from_cli_args():
    cfg = load_config(["-p", "780424"])
    assert cfg.profile_id == 780424
    assert cfg.template == "classic"
    assert cfg.output_dir == "user/780424/badges"
    assert cfg.cache_dir == "user/780424/data"
    assert cfg.hide_if_null is True

def test_load_from_env(monkeypatch):
    monkeypatch.setenv("HTB_PROFILE_ID", "780424")
    cfg = load_config([])
    assert cfg.profile_id == 780424

def test_load_from_config_file(tmp_path, monkeypatch):
    cfg_file = tmp_path / "htb-metrics.yml"
    cfg_file.write_text("profile_id: 780424\ntemplate: terminal\n")
    cfg = load_config(["--config", str(cfg_file)])
    assert cfg.profile_id == 780424
    assert cfg.template == "terminal"

def test_cli_overrides_file(tmp_path):
    cfg_file = tmp_path / "htb-metrics.yml"
    cfg_file.write_text("profile_id: 111111\ntemplate: terminal\n")
    cfg = load_config(["-p", "780424", "--config", str(cfg_file)])
    assert cfg.profile_id == 780424

def test_missing_profile_raises():
    with pytest.raises(ValueError, match="Profile ID is required"):
        load_config(["--config", "/nonexistent.yml"])

def test_invalid_profile_id_raises():
    with pytest.raises(ValueError, match="6-digit"):
        load_config(["-p", "123"])

def test_invalid_template_raises():
    with pytest.raises(ValueError, match="template must be one of"):
        load_config(["-p", "780424", "-t", "nonexistent"])

def test_no_cache_sets_ttl_zero():
    cfg = load_config(["-p", "780424", "--no-cache"])
    assert cfg.cache_ttl == 0


def test_auth_token_from_env_api(monkeypatch):
    monkeypatch.setenv("HTB_API_TOKEN", "api-secret")
    cfg = load_config(["-p", "780424"])
    assert cfg.auth_token == "api-secret"


def test_auth_token_cli_overrides_env(monkeypatch):
    monkeypatch.setenv("HTB_TOKEN", "env-token")
    cfg = load_config(["-p", "780424", "--bearer", "cli-bearer"])
    assert cfg.auth_token == "cli-bearer"


def test_resolve_auth_token_priority():
    assert resolve_auth_token(cli_api_token="a", cli_token="b") == "a"
    assert resolve_auth_token(cli_token="b", file_cfg={"api_token": "c"}) == "b"


def test_auth_token_from_config_file(tmp_path):
    cfg_file = tmp_path / "htb-metrics.yml"
    cfg_file.write_text("profile_id: 780424\ntoken: file-token\n")
    cfg = load_config(["--config", str(cfg_file)])
    assert cfg.auth_token == "file-token"


def test_from_env_requires_dotenv_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="examples/config/.env.example"):
        load_config(["--from-env"])


def test_from_env_loads_profile_and_bearer(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "HTB_PROFILE_ID=780424\nHTB_BEARER=env-bearer\nHTB_TEMPLATE=terminal\n"
        "HTB_HIDE_IF_NULL=false\nHTB_NO_CACHE=true\n"
    )
    cfg = load_config(["--from-env", "-p", "111111", "--bearer", "cli-bearer"])
    assert cfg.profile_id == 780424
    assert cfg.auth_token == "env-bearer"
    assert cfg.template == "terminal"
    assert cfg.hide_if_null is False
    assert cfg.cache_ttl == 0


def test_env_hide_if_null_and_cache_ttl(monkeypatch):
    monkeypatch.setenv("HTB_PROFILE_ID", "780424")
    monkeypatch.setenv("HTB_HIDE_IF_NULL", "false")
    monkeypatch.setenv("HTB_CACHE_TTL", "7200")
    cfg = load_config([])
    assert cfg.hide_if_null is False
    assert cfg.cache_ttl == 7200


def test_env_no_cache(monkeypatch):
    monkeypatch.setenv("HTB_PROFILE_ID", "780424")
    monkeypatch.setenv("HTB_NO_CACHE", "true")
    cfg = load_config([])
    assert cfg.cache_ttl == 0
