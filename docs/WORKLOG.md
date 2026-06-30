# Worklog

Append-only log of project changes. One entry per line, newest date section at the bottom.

## 2026-06-30

- Switched `user_machines` endpoint to `/api/v4/profile/progress/machines/{id}` (replaces removed chart + separate `user_os` endpoint).
- Removed deprecated `team_bracket` public endpoint; added auth-only `team_rankings` via `/api/v4/rankings`.
- Added auth-only fetch targets: `machines` (`/api/v5/machines/`), `user_tracks` (`/api/v5/tracks/`); skipped when no token is set.
- Implemented bearer auth resolution from CLI (`--api-token`, `--token`, `--bearer`), env (`HTB_API_TOKEN`, `HTB_TOKEN`, `HTB_BEARER`), and YAML config keys.
- Updated `fetch.py` with `_request_headers`, `_fetch_optional`, and separate public vs authenticated endpoint loops.
- CLI now prints auth status (`yes` / `no (auth-only endpoints skipped)`).
- Updated `tests/test_fetch.py` for new URLs, auth-skipping behavior, and authenticated fetch test.
- Expanded README with auth secrets, data sources table, and security notes (later moved to `docs/guides/`).
- Added `.env.example` with all supported env vars including boolean flags (`HTB_HIDE_IF_NULL`, `HTB_NO_CACHE`).
- Added `--from-env` and `--env-file` CLI flags; env priority inverts when `--from-env` is used.
- Extended `config.py` with `resolve_auth_token()`, `_env_bool()`, `_env_int()`, and full env var coverage for cache/output settings.
- Added `tests/conftest.py` to isolate `HTB_*` env vars between tests.
- Added config tests for `--from-env`, env booleans, and token priority.
- Documented `avatar_b64.txt` cache file (data URI for SVG template embedding).
- Added template placeholders reference (later moved to `docs/guides/templates.md`).
- Clarified no-fork vs fork GitHub Actions setup; removed stale `uses: yonasuriv/metrics-htb@latest` example.
- Created `references/workflows/htb-metrics-consumer.yml` (checkout profile repo + upstream metrics-htb).
- Created `references/workflows/htb-metrics-fork.yml` (run generator from forked repo).
- Removed active workflows from `.github/workflows/` (templates are copy-paste only).
- Bumped `actions/checkout` from v4 to v6 in workflow templates.
- Migrated package from `htb_metrics/` to `src/htb_metrics/` (src layout).
- Added `src/htb_metrics/paths.py` for repo-root asset path resolution.
- Added `pyproject.toml` with setuptools src layout, dependencies, `htb-metrics` console script, and pytest `pythonpath`.
- Updated `requirements.txt` to `-e .` plus dev deps (`pytest`, `responses`).
- Updated `generate.py` to bootstrap `src/` on `sys.path` for no-install runs.
- Added `tests/test_paths.py` for src-layout path assertions.
- Renamed `references/` to `refs/`.
- Moved `.env.example` and `htb-metrics.yml.example` to `refs/config/`.
- Added `refs/README.md` with layout, copy instructions, and raw GitHub URLs.
- Slimmed root `README.md` to marketing overview linking into `docs/`.
- Added `docs/README.md` documentation index.
- Added `docs/CONTRIBUTING.md`.
- Added `docs/guides/getting-started.md`.
- Added `docs/guides/configuration.md`.
- Added `docs/guides/github-actions.md`.
- Added `docs/guides/development.md`.
- Added `docs/guides/templates.md`.
- Added `docs/guides/data-sources.md`.
- Added `docs/guides/troubleshooting.md`.
- Added `tests/test_refs.py` to verify `refs/` layout and docs guides exist.
- Updated `config.py` `--from-env` error message to point at `refs/config/.env.example`.
- Updated workflow template headers and curl URLs to use `refs/workflows/` paths.
- Committed as `2bd4915` — restructure: src layout, refs/, docs/guides, auth-aware fetch, `--from-env`.

## 2026-06-30 (continued)

- Renamed `refs/` to `examples/` (clearer naming for sample outputs and copy-paste templates).
- Added `examples/badges/` with sample rendered PNG/SVG outputs for template previews (not for copying).
- Rewrote `examples/README.md` to distinguish copyable paths (`config/`, `workflows/`) from preview-only `badges/`.
- Added `.github/assets/` repo logos (`metrics-light.png`, `metrics-dark.png`, `htb.png`) for README header.
- Updated README to use local logo assets and `examples/badges/htb-metrics.classic.png` preview.
- Renamed `tests/test_refs.py` to `tests/test_examples.py` with badge preview assertions.
- Updated all docs, config examples, workflow templates, and curl raw URLs from `refs/` to `examples/`.
- Updated `config.py` `--from-env` hint to `examples/config/.env.example`.
