from __future__ import annotations

from ctrl_cli.ui import Rule, _help_section, console, print_banner


def print_man(hide_banner: bool = False) -> None:
    print_banner(hide_banner=hide_banner)
    console.print(Rule(style="dim green"))
    console.print()
    console.print("[bold]HTB Ctrl — full command reference[/bold]\n")

    console.print(_help_section("GLOBAL FLAGS", "white", [
        ("--from-env",       "Load token/settings from .env (env wins over CLI/YAML)"),
        ("--env-file PATH",  "Dotenv path for --from-env  [default: .env]"),
        ("--config PATH",    "CLI YAML config  [default: htb-cli.yml]"),
        ("--metrics-config", "Metrics YAML fallback for shared token keys"),
        ("--api-token",      "HTB app API token"),
        ("--bearer",         "HTB bearer token"),
        ("--hide-banner",    "Suppress startup banner on help/man"),
    ]))

    console.print(_help_section("MACHINES", "bright_green", [
        ("machines",              "List active machines (cached)"),
        ("  --retired, -r",       "Include retired machines (VIP)"),
        ("  --os, -o OS",         "Filter by OS (linux, windows, …)"),
        ("  --diff, -d LEVEL",    "Filter by difficulty"),
        ("  --search, -s TEXT",   "Search by machine name"),
        ("  --owned",             "Show only fully owned"),
        ("  --pending",           "Show only unowned"),
        ("  --limit, -l N",       "Limit result count"),
        ("  --refresh, -f",       "Force cache refresh"),
        ("machine-info --id, -i", "Detailed machine view (avatar on Kitty)"),
        ("  --debug",             "Dump raw API fields (hidden)"),
        ("submit --id -i --flag -f", "Submit user/root flag"),
        ("  --type, -t user|root",   "Flag type (auto-detected if omitted)"),
        ("  --diff, -d 1-10",        "Perceived difficulty rating"),
    ]))

    console.print(_help_section("LABS", "yellow", [
        ("active",           "Show running machine and IP"),
        ("spawn --id, -i ID", "Start a machine"),
        ("  --vip",            "Use VIP server"),
        ("stop [--id, -i]",   "Stop machine (auto-detect if omitted)"),
        ("reset [--id, -i]",  "Reset machine to initial state"),
    ]))

    console.print(_help_section("METRICS", "blue", [
        ("metrics pull", "Fetch HTB API JSON → user/<id>/data/"),
        ("  -p, --profile ID",     "6-digit HTB profile ID"),
        ("  -t, --template NAME",  "Template name (optional on pull)"),
        ("  -o, --output-dir PATH", "Badge output dir (optional on pull)"),
        ("  --config PATH",         "Metrics YAML  [default: htb-metrics.yml]"),
        ("  --no-cache",            "Disable API response cache"),
        ("  --from-env",            "Load from .env (metrics scope)"),
        ("  --env-file PATH",       "Dotenv for --from-env"),
        ("  --api-token / --token / --bearer", "HTB auth token"),
    ]))

    console.print(_help_section("BADGES", "blue", [
        ("badges generate", "Fetch + render badge → user/<id>/badges/"),
        ("badge generate",  "Alias for badges generate"),
        ("  (same flags as metrics pull)", ""),
    ]))

    console.print(_help_section("DASHBOARD", "bright_blue", [
        ("dashboard",              "Open offline in browser (file picker)"),
        ("dashboard --serve",      "Serve on http://127.0.0.1:8080"),
        ("dashboard --port PORT",  "Port for --serve  [default: 8080]"),
        ("dashboard --new-sheet",  "Create htb_machines.xlsx at repo root"),
        ("  --force",              "Overwrite existing spreadsheet with --new-sheet"),
    ]))

    console.print(_help_section("LEGACY SYNTAX", "dim", [
        ("metrics --pull …",      "Same as metrics pull …"),
        ("metrics --generate …",  "Same as badges generate …"),
        ("metrics --generate-badge …", "Same as badges generate …"),
        ("dashboard new-sheet …", "Same as dashboard --new-sheet …"),
    ]))

    console.print(_help_section("SETTINGS", "magenta", [
        ("auth --token, -t TOKEN", "Save and verify HTB API token"),
        ("profile", "Profile stats, ranking, owns, bloods"),
        ("cache", "Show cache status"),
        ("cache --clear, -c", "Clear machine cache"),
        ("cache --status, -s", "Show cache age and validity"),
    ]))

    console.print(_help_section("ENVIRONMENT", "dim", [
        ("HTB_PROFILE_ID",   "6-digit profile ID (metrics/badges)"),
        ("HTB_API_TOKEN",    "App API token"),
        ("HTB_TOKEN",        "Token alias"),
        ("HTB_BEARER",       "Bearer alias"),
        ("HTB_TEMPLATE",     "Badge template name"),
        ("HTB_OUTPUT_DIR",   "Badge output directory"),
        ("HTB_CACHE_DIR",    "API data cache directory"),
        ("HTB_CACHE_TTL",    "Cache TTL in seconds"),
        ("HTB_NO_CACHE",     "Disable cache when true"),
        ("HTB_HIDE_IF_NULL", "Hide empty badge fields"),
        ("HTBCTRL_SKIP_BOOTSTRAP", "Skip venv bootstrap (CI/tests)"),
    ]))

    console.print(
        "\n  [dim]Per-command Typer help: [white]htbctrl COMMAND --help[/white]\n"
        "  User docs: [white]docs/guides/[/white][/dim]\n"
    )
