import os
from pathlib import Path

import pytest
from dotenv import dotenv_values, load_dotenv as _real_load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_ENV = REPO_ROOT / ".env"


@pytest.fixture(autouse=True)
def isolate_htb_env(monkeypatch):
    """Prevent HTB_* vars from leaking between tests (e.g. after --from-env)."""
    monkeypatch.setenv("HTBCTRL_SKIP_BOOTSTRAP", "1")
    for key in list(os.environ):
        if key.startswith("HTB_"):
            monkeypatch.delenv(key, raising=False)

    def _load_dotenv(*args, **kwargs):
        dotenv_path = kwargs.get("dotenv_path") or (args[0] if args else ".env")
        path = Path(dotenv_path)
        if not path.is_file():
            return False
        if path.resolve() == REPO_ENV.resolve():
            for key, value in (dotenv_values(path) or {}).items():
                if not key.startswith("HTB_"):
                    monkeypatch.setenv(key, value)
            return True
        return _real_load_dotenv(*args, **kwargs)

    monkeypatch.setattr("dotenv.load_dotenv", _load_dotenv)
