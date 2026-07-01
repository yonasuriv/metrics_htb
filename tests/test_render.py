import re
import pytest
from pathlib import Path
from ctrl_metrics.render import inject, render, TemplateNotFoundError

DATA = {
    "user_name": "testuser",
    "user_rank": "Pro Hacker",
    "user_avatar": "https://example.com/avatar.png",
    "user_owns": 61,
    "season_league": "Ruby",
    "last_update": "28 Jun 2026, 00:00 UTC",
    "last_activity": "2 days ago",
}

def test_inject_replaces_known_placeholders():
    html = "<span>$user_name$</span><span>$user_rank$</span>"
    result = inject(html, DATA, hide_if_null=True)
    assert "testuser" in result
    assert "Pro Hacker" in result

def test_inject_hides_null_when_flag_set():
    html = "<span>$level_title$</span>"
    result = inject(html, DATA, hide_if_null=True)
    assert "$level_title$" not in result
    assert result == "<span></span>"

def test_inject_keeps_placeholder_when_hide_false():
    html = "<span>$level_title$</span>"
    result = inject(html, DATA, hide_if_null=False)
    assert "$level_title$" in result

def test_inject_numeric_value_becomes_string():
    html = "<span>$user_owns$</span>"
    result = inject(html, DATA, hide_if_null=True)
    assert "61" in result

def test_template_not_found_raises():
    with pytest.raises(TemplateNotFoundError):
        render("nonexistent-template", DATA, "/tmp/out")
