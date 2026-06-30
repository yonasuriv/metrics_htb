import os

import pytest


@pytest.fixture(autouse=True)
def isolate_htb_env(monkeypatch):
    """Prevent HTB_* vars from leaking between tests (e.g. after --from-env)."""
    for key in list(os.environ):
        if key.startswith("HTB_"):
            monkeypatch.delenv(key, raising=False)
