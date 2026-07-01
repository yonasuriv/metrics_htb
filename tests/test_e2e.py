"""
End-to-end test using the real HTB API.
Requires network access. Skip in CI unless explicitly enabled.

Run locally: pytest tests/test_e2e.py -v -s
"""
import os
import pytest
from pathlib import Path
from ctrl_metrics.config import load_config
from ctrl_metrics.fetch import fetch_all
from ctrl_metrics.dataset import build_dataset

PROFILE_ID = 780424

@pytest.mark.skipif(
    os.environ.get("HTB_E2E") != "1",
    reason="Set HTB_E2E=1 to run live API tests"
)
def test_fetch_real_profile(tmp_path):
    raw = fetch_all(PROFILE_ID, str(tmp_path), cache_ttl=0)
    assert raw["account_id"] is not None
    assert isinstance(raw["profile"]["profile"]["name"], str)
    assert len(raw["profile"]["profile"]["name"]) > 0
    assert raw["experience"]["level"] > 0
    assert raw["season_ranks"]["data"][0]["league"] is not None

@pytest.mark.skipif(
    os.environ.get("HTB_E2E") != "1",
    reason="Set HTB_E2E=1 to run live API tests"
)
def test_dataset_has_no_none_for_core_fields(tmp_path):
    raw = fetch_all(PROFILE_ID, str(tmp_path), cache_ttl=0)
    ds = build_dataset(raw)
    required = ["user_name", "user_rank", "user_avatar", "user_owns",
                "user_system_owns", "user_ranking", "user_points",
                "level_number", "level_title", "season_league", "last_update"]
    for field in required:
        assert ds.get(field) is not None, f"Expected {field} to be set, got None"

@pytest.mark.skipif(
    os.environ.get("HTB_E2E") != "1",
    reason="Set HTB_E2E=1 to run live API tests"
)
def test_render_classic_creates_png(tmp_path):
    from ctrl_metrics.render import render
    raw = fetch_all(PROFILE_ID, str(tmp_path / "cache"), cache_ttl=0)
    ds = build_dataset(raw)
    out = render("classic", ds, str(tmp_path / "output"), hide_if_null=True)
    assert out.exists()
    assert out.stat().st_size > 10_000, "PNG too small — likely blank"
