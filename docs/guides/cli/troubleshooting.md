# Troubleshooting

## Not authenticated / token missing

Run auth and paste your app token:

```bash
python3 src/htb_cli/htbcli.py auth --token YOUR_TOKEN_HERE
```

Token is stored at `~/.config/htbcli/config.json`. See [Getting started](getting-started.md#authenticate).

## HTTP 401 / 403 from HTB API

- Confirm the token is valid at [HTB Settings → API Key](https://app.hackthebox.com/account-settings)
- Regenerate the token if it was revoked
- Re-run `auth --token ...`

## Avatar images not showing

Inline images require [Kitty](https://sw.kovidgoyal.net/kitty/) with `kitten icat` on your PATH. All other CLI output works without Kitty.

## Stale machine list

Force a refresh or clear cache:

```bash
python3 src/htb_cli/htbcli.py machines --refresh
python3 src/htb_cli/htbcli.py cache --clear
```

## Submit flag errors

- Ensure the machine ID is correct (`machine-info --id <id>`)
- User flag must be submitted before root (unless using `--type root` explicitly)
- If both flags are owned, the CLI warns instead of submitting again

## Still stuck?

Open an issue with the command you ran, machine ID (if relevant), and error output (redact your token).
