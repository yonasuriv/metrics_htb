import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HTBCTRL = REPO_ROOT / "htbctrl.py"


def test_init_requires_venv(tmp_path, monkeypatch):
    import htbctrl

    monkeypatch.setattr(htbctrl, "REPO_ROOT", tmp_path)
    with pytest.raises(SystemExit) as exc:
        htbctrl.cmd_init()
    assert exc.value.code == 1


def test_init_creates_env_and_config_dir(tmp_path, monkeypatch):
    import htbctrl

    venv_python = tmp_path / ".venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.touch()

    env_example_dir = tmp_path / "examples" / "config"
    env_example_dir.mkdir(parents=True)
    (env_example_dir / ".env.example").write_text("HTB_PROFILE_ID=\n")

    monkeypatch.setattr(htbctrl, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    htbctrl.cmd_init()

    assert (tmp_path / ".config" / "htb-ctrl" / "cli").is_dir()
    assert (tmp_path / ".env").read_text() == "HTB_PROFILE_ID=\n"


def test_setup_init_flag_parsed():
    import htbctrl

    args = htbctrl.build_parser().parse_args(["setup", "--init"])
    assert args.command == "setup"
    assert args.init is True


def test_init_cli_parses():
    import htbctrl

    args = htbctrl.build_parser().parse_args(["init"])
    assert args.command == "init"
