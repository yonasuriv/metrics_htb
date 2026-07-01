# GitHub Actions workflow templates

Copy one file to **your** repo as `.github/workflows/htb-metrics.yml`.

| File | Use when |
|------|----------|
| [htb-metrics-consumer.yml](htb-metrics-consumer.yml) | **Recommended** — profile repo, pulls generator from `yonasuriv/htb-ctrl` |
| [htb-metrics-fork.yml](htb-metrics-fork.yml) | You forked the full `htb-ctrl` repo |

Full setup: [docs/guides/badge-github-actions.md](../../docs/guides/badge-github-actions.md).

```bash
mkdir -p .github/workflows
curl -o .github/workflows/htb-metrics.yml \
  https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/workflows/htb-metrics-consumer.yml
```
