import os
from pathlib import Path

import pytest

import ctrl_cli.bootstrap as boot


def test_skip_bootstrap_env(monkeypatch):
    monkeypatch.setenv("HTBCTRL_SKIP_BOOTSTRAP", "1")
    assert boot.should_bootstrap() is False


def test_skip_bootstrap_ci(monkeypatch):
    monkeypatch.delenv("HTBCTRL_SKIP_BOOTSTRAP", raising=False)
    monkeypatch.setenv("CI", "true")
    assert boot.should_bootstrap() is False


def test_running_in_venv_false_when_only_symlink_matches_system_python(tmp_path, monkeypatch):
    import sys

    monkeypatch.setattr(boot, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(boot, "VENV_DIR", tmp_path / ".venv")
    venv_bin = tmp_path / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    venv_py = venv_bin / "python"
    venv_py.symlink_to(Path(sys.executable))
    assert boot.running_in_venv() is False


def test_repo_root_is_repo_not_src():
    assert boot.REPO_ROOT.name != "src"
    assert (boot.REPO_ROOT / "htbctrl.py").is_file()
    assert (boot.REPO_ROOT / "requirements.txt").is_file()

