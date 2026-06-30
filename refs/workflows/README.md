# GitHub Actions workflow templates

Copy one file to **your** repo as `.github/workflows/htb-metrics.yml`.

| File | Use when |
|------|----------|
| [htb-metrics-consumer.yml](htb-metrics-consumer.yml) | **Recommended** — profile repo, pulls generator from `yonasuriv/metrics-htb` |
| [htb-metrics-fork.yml](htb-metrics-fork.yml) | You forked the full `metrics-htb` repo |

Full setup: [docs/guides/github-actions.md](../../docs/guides/github-actions.md).

```bash
mkdir -p .github/workflows
curl -o .github/workflows/htb-metrics.yml \
  https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/refs/workflows/htb-metrics-consumer.yml
```
