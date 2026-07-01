# Troubleshooting

## Profile ID is required

Set `HTB_PROFILE_ID` in `.env`, GitHub Actions secrets, or pass `-p <id>`.

```bash
cp examples/config/.env.example .env
python htbm.py metrics --generate --from-env
```

## --from-env requires .env

Create `.env` at the repo root from the example:

```bash
cp examples/config/.env.example .env
```

## HTTP 403 / profile is private

Set your HTB profile to **Public**: Profile → Settings → Privacy.

## No .badge element found

HTML template rendering failed. Ensure the template has a root `.badge` element and vendor icons exist:

```bash
python scripts/download_icons.py
```

## Empty or N/A fields

Some data may be null (no team, no season activity). Set `HTB_HIDE_IF_NULL=false` or `hide_if_null: false` to show empty placeholders instead of hiding them.

## Playwright / Chromium errors

Install the browser:

```bash
playwright install chromium --with-deps
```

## Template not found

Check available templates:

```bash
python htbm.py metrics --generate -t nonexistent   # lists valid names in error
```

Templates live in `assets/templates/html/` and `assets/templates/svg/`.

## GitHub Actions: secret not set

Add `HTB_PROFILE_ID` under repo Settings → Secrets and variables → Actions.

## GitHub Actions: workflow not running

Ensure the workflow file is at `.github/workflows/*.yml` in **your** profile repo, not in `yonasuriv/metrics-htb` unless you forked it.

## Auth endpoints return nothing

Auth-only data requires an HTB app token. Without `HTB_API_TOKEN` / `HTB_TOKEN` / `HTB_BEARER`, machines/tracks/rankings are intentionally skipped.

## Still stuck?

Open an issue with template name, profile ID (last 2 digits redacted), and error output.
