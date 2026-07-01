from ctrl_cli.argv import normalize_argv


def test_legacy_metrics_pull():
    assert normalize_argv(["metrics", "--pull", "-p", "123456"]) == [
        "metrics",
        "pull",
        "-p",
        "123456",
    ]


def test_legacy_metrics_generate():
    assert normalize_argv(["metrics", "--generate", "-t", "classic"]) == [
        "badges",
        "generate",
        "-t",
        "classic",
    ]


def test_legacy_generate_badge_flag():
    assert normalize_argv(["metrics", "--generate-badge"]) == ["badges", "generate"]


def test_modern_argv_unchanged():
    argv = ["metrics", "pull", "-p", "123456"]
    assert normalize_argv(argv) == argv


def test_badge_alias():
    assert normalize_argv(["badge", "generate", "-p", "123456"]) == [
        "badges",
        "generate",
        "-p",
        "123456",
    ]


def test_legacy_dashboard_new_sheet():
    assert normalize_argv(["dashboard", "new-sheet"]) == ["dashboard", "--new-sheet"]
