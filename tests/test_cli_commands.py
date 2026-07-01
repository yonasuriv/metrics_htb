import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HTBCTRL = REPO_ROOT / "htbctrl.py"
VENV_PY = REPO_ROOT / ".venv" / "bin" / "python"
ENV = {**os.environ, "HTBCTRL_SKIP_BOOTSTRAP": "1"}


def _help(*args: str) -> str:
    proc = subprocess.run(
        [str(VENV_PY), str(HTBCTRL), *args, "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=ENV,
    )
    return proc.stdout + proc.stderr


def test_metrics_pull_help():
    assert "pull" in _help("metrics")


def test_badges_generate_help():
    out = _help("badges")
    assert "generate" in out


def test_dashboard_help():
    assert "dashboard" in _help("dashboard")
