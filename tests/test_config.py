import pytest
import os
from htb_metrics.config import load_config, Config

def test_load_from_cli_args():
    cfg = load_config(["-p", "780424"])
    assert cfg.profile_id == 780424
    assert cfg.template == "classic"
    assert cfg.output_dir == "output"
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
