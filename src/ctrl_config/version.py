from __future__ import annotations

import functools
import tomllib

from ctrl_config.paths import REPO_ROOT


@functools.lru_cache(maxsize=1)
def project_version() -> str:
    """Return [project].version from pyproject.toml at the repo root."""
    pyproject = REPO_ROOT / "pyproject.toml"
    if pyproject.is_file():
        # Use load(rb) — works on 3.11+; loads(bytes) breaks on 3.13.
        with pyproject.open("rb") as fp:
            data = tomllib.load(fp)
        return str(data["project"]["version"])

    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("htb-ctrl")
    except PackageNotFoundError:
        return "0.0.0"
