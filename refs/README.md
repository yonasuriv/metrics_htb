# Reference files

Files in this directory are **templates** — copy them into your own project. Nothing here runs automatically from the metrics-htb repository.

## Layout

```
refs/
├── config/
│   ├── .env.example              → copy to repo root as .env
│   └── htb-metrics.yml.example   → copy to repo root as htb-metrics.yml
└── workflows/
    ├── htb-metrics-consumer.yml  → copy to .github/workflows/ (no fork)
    ├── htb-metrics-fork.yml      → copy to .github/workflows/ (fork)
    └── README.md
```

## Config examples

```bash
cp refs/config/.env.example .env
cp refs/config/htb-metrics.yml.example htb-metrics.yml
```

Edit at least `HTB_PROFILE_ID`. See [Configuration](../docs/guides/configuration.md).

## Workflow templates

See [GitHub Actions guide](../docs/guides/github-actions.md) or [workflows/README.md](workflows/README.md).

## Raw URLs (GitHub)

Replace `@main` with a tag or SHA to pin a version.

| File | URL |
|------|-----|
| Consumer workflow | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/refs/workflows/htb-metrics-consumer.yml` |
| Fork workflow | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/refs/workflows/htb-metrics-fork.yml` |
| `.env` example | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/refs/config/.env.example` |
| YAML example | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/refs/config/htb-metrics.yml.example` |
