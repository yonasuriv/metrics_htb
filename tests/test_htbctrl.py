from pathlib import Path

import pytest

import ctrl_cli.bootstrap as boot


def test_silent_init_creates_config_dir_and_env(tmp_path, monkeypatch):
    monkeypatch.setattr(boot, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    env_example_dir = tmp_path / "examples" / "config"
    env_example_dir.mkdir(parents=True)
    (env_example_dir / ".env.example").write_text("HTB_PROFILE_ID=\n")

    boot.silent_init()

    assert (tmp_path / ".config" / "htb-ctrl" / "cli").is_dir()
    assert (tmp_path / ".env").read_text() == "HTB_PROFILE_ID=\n"
    assert (tmp_path / "htb_machines.xlsx").is_file()


def test_silent_init_skips_existing_env(tmp_path, monkeypatch):
    monkeypatch.setattr(boot, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    (tmp_path / ".env").write_text("existing=1\n")

    boot.silent_init()
    assert (tmp_path / ".env").read_text() == "existing=1\n"


def test_should_bootstrap_respects_skip_flag(monkeypatch):
    monkeypatch.setenv("HTBCTRL_SKIP_BOOTSTRAP", "1")
    assert boot.should_bootstrap() is False
