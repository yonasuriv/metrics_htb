from __future__ import annotations

_LEGACY_METRICS_FLAGS = {
    "--pull": ("metrics", "pull"),
    "--generate": ("badges", "generate"),
    "--generate-badge": ("badges", "generate"),
}

_COMMAND_ALIASES = {
    "badge": "badges",
}

_ROOT_COMMANDS = frozenset({
    "auth", "machines", "machine-info", "submit", "active", "spawn", "stop", "reset",
    "profile", "cache", "metrics", "badges", "badge", "dashboard",
})

_OPTION_TAKES_VALUE = frozenset({
    "--env-file", "--config", "--metrics-config", "--api-token", "--bearer",
})


def wants_root_help(argv: list[str]) -> bool:
    """True when argv is root-level --help/-h with no subcommand."""
    if not argv or ("--help" not in argv and "-h" not in argv):
        return False
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in _OPTION_TAKES_VALUE:
            i += 2
            continue
        if token in ("--from-env", "--hide-banner", "-h", "--help"):
            i += 1
            continue
        if token.startswith("-"):
            i += 1
            continue
        return token not in _ROOT_COMMANDS
    return True


def apply_global_argv(argv: list[str]) -> str | None:
    """Parse root global flags from argv and set the runtime token."""
    from ctrl_cli.cache import set_runtime_token
    from ctrl_cli.config import bootstrap_cli_config

    from_env = "--from-env" in argv
    env_file = ".env"
    config = "htb-cli.yml"
    metrics_config = "htb-metrics.yml"
    api_token = bearer = None

    i = 0
    while i < len(argv):
        token = argv[i]
        if token == "--env-file" and i + 1 < len(argv):
            env_file = argv[i + 1]
            i += 2
        elif token == "--config" and i + 1 < len(argv):
            config = argv[i + 1]
            i += 2
        elif token == "--metrics-config" and i + 1 < len(argv):
            metrics_config = argv[i + 1]
            i += 2
        elif token == "--api-token" and i + 1 < len(argv):
            api_token = argv[i + 1]
            i += 2
        elif token == "--bearer" and i + 1 < len(argv):
            bearer = argv[i + 1]
            i += 2
        else:
            i += 1

    try:
        token = bootstrap_cli_config(
            from_env=from_env,
            env_file=env_file,
            cli_config=config,
            metrics_config=metrics_config,
            cli_api_token=api_token,
            cli_bearer=bearer,
        )
    except ValueError:
        token = None
    set_runtime_token(token)
    return token


def normalize_argv(argv: list[str]) -> list[str]:
    """Map legacy flags and command aliases to current subcommands."""
    normalized: list[str] = []
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in _COMMAND_ALIASES:
            normalized.append(_COMMAND_ALIASES[token])
            i += 1
            continue
        if token == "metrics" and i + 1 < len(argv):
            mapping = _LEGACY_METRICS_FLAGS.get(argv[i + 1])
            if mapping is not None:
                normalized.extend(mapping)
                i += 2
                continue
        if token == "dashboard" and i + 1 < len(argv) and argv[i + 1] == "new-sheet":
            normalized.extend(["dashboard", "--new-sheet"])
            i += 2
            continue
        normalized.append(token)
        i += 1
    return normalized
