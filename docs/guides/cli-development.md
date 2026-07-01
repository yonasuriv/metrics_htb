# Development

## Project layout

```
htb-ctrl/
└── src/ctrl_cli/
    ├── cli.py              # Typer entry point
    ├── bootstrap.py        # venv bootstrap + repo paths
    ├── config.py           # thin wrapper → ctrl_config
    ├── api.py, cache.py, ui.py
    ├── components/
    │   ├── terminal.py     # auth, machines, submit, spawn, …
    │   ├── metrics.py      # metrics pull
    │   ├── badges.py       # badges generate
    │   ├── dashboard.py    # dashboard serve
    │   └── __banner__      # startup ASCII art
```

## How it works

| Component | Description |
|-----------|-------------|
| **API** | HTB API v4 (`labs.hackthebox.com/api/v4`) |
| **UI rendering** | [Rich](https://github.com/Textualize/rich) panels, tables, progress bars, colors |
| **Image support** | Kitty `kitten icat` with `--place` for precise positioning |
| **Layout** | ANSI escape sequences (DSR for cursor, CUP for positioning) |
| **Cache** | Simple JSON file with per-key TTL |

## Tech stack

| Component | Technology |
|-----------|------------|
| CLI framework | [Typer](https://typer.tiangolo.com/) |
| Terminal UI | [Rich](https://github.com/Textualize/rich) |
| HTTP client | [Requests](https://docs.python-requests.org/) |
| Image rendering | [Kitty](https://sw.kovidgoyal.net/kitty/) `kitten icat` |
| API | HTB API v4 |

## Contributing

Found a bug or have an idea? [Open an issue](https://github.com/yonasuriv/htb-ctrl/issues).

Want to contribute code? Fork → branch → PR. All contributions welcome.

## Author

**Jean Pierre Montalvo** (yonasuriv)

[![GitHub](https://img.shields.io/badge/GitHub-K--4yser-181717?style=flat&logo=github)](https://github.com/yonasuriv)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-jean--montalvo-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/jean-montalvo)
[![HTB](https://img.shields.io/badge/Hack%20The%20Box-K--4yser-9FEF00?style=flat&logo=hackthebox&logoColor=white)](https://app.hackthebox.com/public/users/416937)

## License

MIT — see [LICENSE](../../LICENSE).
