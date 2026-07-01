# Getting started

## Requirements

- Python 3.11+
- [Playwright](https://playwright.dev/python/) Chromium (for PNG rendering)
- Public HTB profile (Profile → Settings → Privacy)

## Local install

### Quick setup

```bash
git clone https://github.com/yonasuriv/htb-ctrl.git
cd htb-ctrl
htbctrl --help
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

First `htbctrl` run creates `.venv`, installs dependencies, and runs Playwright Chromium setup once.

### Manual install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

`requirements.txt` installs the package in editable mode (`-e .`) from `src/ctrl_metrics/`.

## Generate your first badge

### Option A — `.env` (recommended)

```bash
cp examples/config/.env.example .env
# Edit .env: set HTB_PROFILE_ID (6 digits)
htbctrl badges generate --from-env
```

### Option B — CLI flags

```bash
htbctrl badges generate -p YOUR_PROFILE_ID -t classic
```

### Option C — YAML config

```bash
cp examples/config/htb-metrics.yml.example htb-metrics.yml
# Edit htb-metrics.yml
htbctrl badges generate
```

Output appears in `user/<profile_id>/badges/` (e.g. `user/780424/badges/htb-metrics.classic.png`).

## Pull data only

Fetch HTB API responses to JSON without rendering a badge:

```bash
htbctrl metrics pull -p YOUR_PROFILE_ID
# or
htbctrl metrics pull --from-env
```

Data is stored under `user/<profile_id>/data/`.

## Embed in README

```markdown
![HTB Metrics](user/780424/badges/htb-metrics.classic.png)
```

Replace `780424` with your profile ID.

## GitHub Actions (no fork)

Automate daily updates in your profile repo without forking this project:

1. Add secrets: `HTB_PROFILE_ID` (required), optional `HTB_API_TOKEN` / `HTB_TOKEN` / `HTB_BEARER`
2. Copy the consumer workflow:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/htb-metrics.yml \
  https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/workflows/htb-metrics-consumer.yml
```

3. Push, run **Actions → HTB Metrics**, embed the PNG path in your README.

Details: [GitHub Actions](badge-github-actions.md).

## Optional app token

Create an app token at [HTB Settings → App Tokens](https://app.hackthebox.com/profile/settings) to fetch auth-only data (machines catalog, tracks, team rankings). Without it, public profile data still works.

See [Configuration](configuration.md#authentication).

## Next steps

- [Configuration](configuration.md) — all flags and env vars
- [Templates](badge-templates.md) — pick a theme
- [Troubleshooting](badge-troubleshooting.md) — if something fails
