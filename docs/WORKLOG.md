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
- Clarified no-fork vs fork GitHub Actions setup; removed stale `uses: yonasuriv/htb-ctrl@latest` example.
- Created `references/workflows/htb-metrics-consumer.yml` (checkout profile repo + upstream htb-ctrl).
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
- Committed as `fe034fd` on `dev` — add HTB CLI and dashboard with split English documentation; badge guides under `docs/guides/badge/`, CLI/dashboard guides, monorepo README.

## 2026-06-30 (htbm + user paths)

- Translated `src/htb_dashboard/index.html` to English (UI strings, DataTables locale, column header labels).
- Fixed dashboard infinite loading: added fetch error handling, `file://` detection, and manual `.xlsx` file picker fallback.
- Moved per-user cache from `.cache/{profile_id}/` to `user/{profile_id}/data/` (`paths.user_data_dir`, `default_cache_dir`).
- Moved badge output from `output/` to `user/{profile_id}/badges/` (`paths.user_badges_dir`, `default_output_dir`).
- Updated `fetch.py` to treat `cache_dir` as the data directory directly (no nested profile subfolder).
- Updated `config.py` defaults to derive data/badge paths from the resolved profile ID.
- Added `htbctrl.py` unified entry point: `setup`, `cli`, `metrics --pull`, `metrics --generate`, `dashboard`, `dashboard --serve`.
- Refactored `htb_metrics/cli.py` into `run_pull()` (JSON fetch only) and `run_generate()` (full badge workflow).
- Kept `generate.py` as a backward-compatible alias for `htbctrl.py metrics --generate`.
- Updated GitHub Actions workflow templates to use `htbctrl.py` and commit `user/$HTB_PROFILE_ID/badges/`.
- Updated `.gitignore` to ignore `user/` instead of only `.cache/` and `output/`.
- Updated README, docs (badge/cli/dashboard), examples, CONTRIBUTING, and tests for new paths and commands.

## 2026-07-01

- Moved sample spreadsheet to `examples/sheets/htb_machines_example.xlsx` and added headers-only `htb_machines_template.xlsx`.
- Switched dashboard data source from `src/htb_dashboard/htb_machines_UPDATE.xlsx` to repo-root `htb_machines.xlsx` (gitignored).
- Added `python htbctrl.py dashboard --new-sheet` to create a clean header-only spreadsheet at the repo root.
- Updated dashboard HTTP server to serve `htb_machines.xlsx` from the repo root alongside `index.html`.
- Hid the manual upload card after a spreadsheet loads successfully (URL fetch or file picker).
- Added `src/htb_cli/config.py` with env/YAML token resolution shared with `htb-metrics.yml`.
- Added `examples/config/htb-cli.yml.example` and documented shared token priority in CLI configuration guide.
- Extended `.env.example` notes for shared metrics/CLI token vars and `--from-env` usage.
- Updated README, dashboard/cli docs, `examples/README.md`, tests, and `.gitignore` for the new sheet layout.
- Removed per-package README stubs under `src/` (documented in root README and `docs/` instead).

## 2026-07-01 (continued)

- Moved CLI config/cache from `~/.config/htbcli` to `~/.config/htb-ctrl/cli`.
- Switched spreadsheet column headers to English in `sheet.py`, template, and example sheets.

## 2026-07-01 (rename to htb-ctrl)

- Renamed repository from `metrics-htb` to `htb-ctrl` (GitHub: `yonasuriv/htb-ctrl`).
- Renamed unified entry point `htbm.py` → `htbctrl.py`; CLI config dir `~/.config/htbm` → `~/.config/htb-ctrl`.
- Added `python htbctrl.py init` (`.env` from example, config dir) and `setup --init` (setup + init).
- Updated README, docs, examples, workflow templates (`htb_ctrl_ref`, `_htb-ctrl` checkout path), and tests.
