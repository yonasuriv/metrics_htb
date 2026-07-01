from __future__ import annotations

_LEGACY_METRICS_FLAGS = {
    "--pull": ("metrics", "pull"),
    "--generate": ("badges", "generate"),
    "--generate-badge": ("badges", "generate"),
}

_COMMAND_ALIASES = {
    "badge": "badges",
}


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
