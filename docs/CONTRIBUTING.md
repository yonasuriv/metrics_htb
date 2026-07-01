# Contributing

Thanks for helping improve HTB Ctrl.

## Before you start

- Read [Development](guides/badge-development.md) for project layout, `htbctrl` commands, and tests
- Check existing issues and PRs
- Keep changes focused — prefer small, reviewable diffs

## Development workflow

```bash
git clone https://github.com/yonasuriv/htb-ctrl.git
cd htb-ctrl
htbctrl --help
source .venv/bin/activate
python -m pytest tests/ --ignore=tests/test_e2e.py
```

## Pull requests

1. Fork the repo and create a feature branch
2. Add or update tests for behavior changes
3. Run the test suite locally
4. Update docs in `docs/guides/` if user-facing behavior changes
5. Update `examples/` templates if workflow or config examples change
6. Open a PR with a clear description and test plan

## Code style

- Match existing patterns in `src/ctrl_metrics/`, `src/ctrl_cli/`, and `src/ctrl_config/`
- Minimal scope — avoid unrelated refactors
- No committed secrets, `.env`, or personal profile IDs in examples

## Documentation

- User docs: `docs/guides/` (flat files, no subfolders)
- Copy-paste templates: `examples/`
- Marketing overview: root `README.md` (keep brief; link to docs)

## Templates

New badge templates go in `assets/templates/html/` or `assets/templates/svg/`. Document placeholders in [badge-templates.md](guides/badge-templates.md).

## Questions

Open a GitHub issue for bugs, feature requests, or HTB API changes.
