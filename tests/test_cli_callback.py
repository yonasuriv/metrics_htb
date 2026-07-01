import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HTBCTRL = REPO_ROOT / "htbctrl.py"
VENV_PY = REPO_ROOT / ".venv" / "bin" / "python"
_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _plain(text: str) -> str:
    return _ANSI.sub("", text)


def test_cli_help_lists_global_token_options():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    out = _plain(proc.stdout + proc.stderr)
    assert "--from-env" in out
    assert "--api-token" in out
    assert "--bearer" in out
    assert "metrics" in out
    assert "badges" in out
    assert "dashboard" in out


def test_cli_banner_lists_metrics_and_badges():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    out = _plain(proc.stdout + proc.stderr)
    assert "metrics" in out
    assert "badges" in out
    assert "dashboard" in out
    assert "metrics pull" not in out
    assert "badges generate" not in out
    assert "dashboard --serve" not in out
    assert "SETTINGS" in out
    assert "LABS" in out
    assert "LAB CONTROL" not in out
    assert "AUTHENTICATION" not in out
    assert "Global:" not in out
    assert "Legacy:" not in out


def test_man_shows_full_reference():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "--hide-banner", "man"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    assert proc.returncode == 0
    out = _plain(proc.stdout + proc.stderr)
    assert "--from-env" in out
    assert "--api-token" in out
    assert "metrics --pull" in out
    assert "HTB_PROFILE_ID" in out
    assert "machines --retired" in out or "--retired" in out


def test_metrics_pull_accepts_profile_flag():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "metrics", "pull", "-p", "12345"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    out = _plain(proc.stdout + proc.stderr)
    assert "profile_id must be a 6-digit number" in out or "Config error" in out
    assert "No such option" not in out


def test_legacy_metrics_pull_flag():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "metrics", "--pull", "-p", "12345"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    out = _plain(proc.stdout + proc.stderr)
    assert "profile_id must be a 6-digit number" in out or "Config error" in out
    assert "No such command" not in out


def test_metrics_pull_help_shows_profile_flag():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "metrics", "pull", "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    out = _plain(proc.stdout + proc.stderr)
    assert "--profile" in out or "-p" in out
    assert "6-digit" in out


def test_badge_alias_help():
    if not VENV_PY.is_file():
        pytest.skip("venv required")
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), "badge", "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**dict(os.environ), "HTBCTRL_SKIP_BOOTSTRAP": "1"},
    )
    assert proc.returncode == 0
    out = _plain(proc.stdout + proc.stderr)
    assert "generate" in out
