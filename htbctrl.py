#!/usr/bin/env python3
"""HTB Ctrl Cli."""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC = REPO_ROOT / "src"

if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def main(argv: list[str] | None = None) -> None:
    from ctrl_cli import bootstrap as boot

    argv = list(sys.argv[1:] if argv is None else argv)

    if boot.should_bootstrap() and not boot.running_in_venv():
        boot.ensure_runtime(quiet=True)
        boot.silent_init()
        venv_py = boot.venv_python()
        os.execv(str(venv_py), [str(venv_py), __file__, *argv])

    from ctrl_cli.argv import normalize_argv
    from ctrl_cli.cli import app

    import typer.main

    argv = normalize_argv(argv)
    cmd = typer.main.get_command(app)
    raise SystemExit(cmd(args=argv, standalone_mode=False, prog_name="htbctrl"))


if __name__ == "__main__":
    main()
