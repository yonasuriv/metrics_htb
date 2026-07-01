# GitHub Actions

This repository does **not** ship workflows under `.github/workflows/`. Copy a template from [`examples/workflows/`](../../examples/workflows/) into **your** repo.

## Consumer workflow (no fork) — recommended

Your profile repo keeps only a workflow file + secrets. Each run checks out `yonasuriv/metrics-htb` and writes PNGs to `user/<profile_id>/badges/`.

### Setup

1. **Secrets** (Settings → Secrets and variables → Actions):
   - `HTB_PROFILE_ID` — required
   - Optional: `HTB_API_TOKEN`, `HTB_TOKEN`, or `HTB_BEARER`

2. **Workflow file**:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/htb-metrics.yml \
  https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/examples/workflows/htb-metrics-consumer.yml
```

Or copy [`examples/workflows/htb-metrics-consumer.yml`](../../examples/workflows/htb-metrics-consumer.yml) manually.

3. Commit, push, run **Actions → HTB Metrics**.

4. README embed:

```markdown
![HTB Metrics](user/780424/badges/htb-metrics.classic.png)
```

Replace `780424` with your profile ID.

### Pin generator version

The workflow input `metrics_htb_ref` (default `main`) selects which git ref of `metrics-htb` to use. Pin a tag or SHA for reproducible builds.

## Fork workflow

If you forked the full repository, use [`examples/workflows/htb-metrics-fork.yml`](../../examples/workflows/htb-metrics-fork.yml) instead. It runs `htbm.py metrics --generate` from the checked-out fork (no second checkout).

## Schedule

Both templates run daily at **00:00 UTC** (`cron: '0 0 * * *'`). Edit the cron line to change timing.

## What the workflow does

1. Check out your repo (and `metrics-htb` for consumer template)
2. `pip install -r requirements.txt` (editable install of `src/htb_metrics`)
3. `playwright install chromium --with-deps`
4. `python htbm.py metrics --generate -p $HTB_PROFILE_ID -t $TEMPLATE`
5. Commit `user/$HTB_PROFILE_ID/badges/` if changed (`[skip ci]`)

## Notes

- Uses `actions/checkout@v6`
- Requires `contents: write` permission to push badge updates
- See [Configuration](configuration.md) for secrets and tokens
