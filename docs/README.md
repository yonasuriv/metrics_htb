# Documentation

User and contributor documentation for **Metrics HTB** — badges, CLI, and browser dashboard.

Entry point: [`htbm.py`](../htbm.py) at the repo root (`setup`, `cli`, `metrics`, `dashboard`).

## Badges (`src/htb_metrics`)

- [Getting started](guides/badge/getting-started.md) — install, generate locally, embed in README
- [Configuration](guides/badge/configuration.md) — CLI flags, `.env`, YAML, priority rules
- [GitHub Actions](guides/badge/github-actions.md) — automated daily updates
- [Templates](guides/badge/templates.md) — available themes and `$placeholder$` reference
- [Data sources](guides/badge/data-sources.md) — HTB API endpoints (public vs auth)
- [Development](guides/badge/development.md) — src layout, tests, project structure
- [Troubleshooting](guides/badge/troubleshooting.md) — common errors and fixes

## CLI (`src/htb_cli`)

- [Getting started](guides/cli/getting-started.md) — install, authenticate, first commands
- [Usage](guides/cli/usage.md) — machines, flags, lab control, profile, cache
- [Configuration](guides/cli/configuration.md) — config files, cache, avatar sizes
- [Development](guides/cli/development.md) — architecture, stack, contributing
- [Troubleshooting](guides/cli/troubleshooting.md) — common errors

## Dashboard (`src/htb_dashboard`)

- [Getting started](guides/dashboard/getting-started.md) — setup and project layout
- [Features](guides/dashboard/features.md) — table, badges, DataTables, Excel loading
- [Customization](guides/dashboard/customization.md) — add techniques and tweak styles
- [Development](guides/dashboard/development.md) — tech stack and data flow

## Reference files

Copy-paste templates live under [`examples/`](../examples/README.md) (`config/`, `workflows/`). Badge previews in `examples/badges/` are for documentation only.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
