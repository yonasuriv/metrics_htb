from __future__ import annotations
import sys
from colorama import Fore, Style, init as _init
from .config import load_config
from .fetch import fetch_all, FetchError
from .dataset import build_dataset
from .render import render, render_svg, TemplateNotFoundError, SVG_TEMPLATES_DIR


def main() -> None:
    _init()
    try:
        cfg = load_config()
    except (ValueError, SystemExit) as e:
        if isinstance(e, ValueError):
            print(f"\n{Fore.RED}[E]{Style.RESET_ALL} Config error: {e}")
            sys.exit(1)
        raise

    print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} HTB Metrics Generator\n")
    print(f"    Profile  : {Fore.CYAN}{cfg.profile_id}{Style.RESET_ALL}")
    print(f"    Template : {Fore.CYAN}{cfg.template}{Style.RESET_ALL}")
    print(f"    Output   : {Fore.CYAN}{cfg.output_dir}{Style.RESET_ALL}")
    auth_status = (
        f"{Fore.GREEN}yes{Style.RESET_ALL}"
        if cfg.auth_token
        else f"{Fore.YELLOW}no (auth-only endpoints skipped){Style.RESET_ALL}"
    )
    print(f"    Auth     : {auth_status}")

    print(f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Fetching HTB data...")
    try:
        raw = fetch_all(
            cfg.profile_id,
            cfg.cache_dir,
            cfg.cache_ttl,
            auth_token=cfg.auth_token,
        )
    except FetchError as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} {e}")
        sys.exit(1)

    print(f"{Fore.BLUE}[-]{Style.RESET_ALL} Building dataset...")
    data = build_dataset(raw)

    name = data.get("user_name", "unknown")
    rank = data.get("user_rank", "")
    level = data.get("level_title", "")
    league = data.get("season_league", "")
    print(f"\n    {Fore.MAGENTA}{name}{Style.RESET_ALL} Lv.{data.get('level_number','')} {level} ({rank}) [{league}]")

    is_svg = (SVG_TEMPLATES_DIR / f"{cfg.template}.svg").exists()

    print(f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Rendering {cfg.template} template...")
    try:
        if is_svg:
            svg_path, png_path = render_svg(cfg.template, data, cfg.output_dir, cfg.hide_if_null)
            print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} SVG: {svg_path}")
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} PNG: {png_path}")
        else:
            out_path = render(cfg.template, data, cfg.output_dir, cfg.hide_if_null)
            print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Saved: {out_path}")
    except TemplateNotFoundError as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} Render error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
