from __future__ import annotations
import sys
from colorama import Fore, Style, init as _init

from .config import load_config
from .fetch import fetch_all, FetchError
from .dataset import build_dataset
from .render import render, TemplateNotFoundError


def main() -> None:
    _init()
    try:
        cfg = load_config()
    except (ValueError, SystemExit) as e:
        if isinstance(e, ValueError):
            print(f"{Fore.RED}[E]{Style.RESET_ALL} Config error: {e}")
            sys.exit(1)
        raise

    print(f"\n{Fore.BLUE}[*]{Style.RESET_ALL} HTB Metrics Generator")
    print(f"    Profile  : {Fore.CYAN}{cfg.profile_id}{Style.RESET_ALL}")
    print(f"    Template : {Fore.CYAN}{cfg.template}{Style.RESET_ALL}")
    print(f"    Output   : {Fore.CYAN}{cfg.output_dir}{Style.RESET_ALL}")

    print(f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Fetching HTB data...")
    try:
        raw = fetch_all(cfg.profile_id, cfg.cache_dir, cfg.cache_ttl)
    except FetchError as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} {e}")
        sys.exit(1)

    print(f"{Fore.BLUE}[-]{Style.RESET_ALL} Building dataset...")
    data = build_dataset(raw)

    name = data.get("user_name", "unknown")
    rank = data.get("user_rank", "")
    level = data.get("level_title", "")
    league = data.get("season_league", "")
    print(f"    {Fore.GREEN}{name}{Style.RESET_ALL}  {rank}  Lv.{data.get('level_number','')} {level}  {league}")

    print(f"\n{Fore.BLUE}[-]{Style.RESET_ALL} Rendering {cfg.template} template...")
    try:
        out_path = render(cfg.template, data, cfg.output_dir, cfg.hide_if_null)
    except TemplateNotFoundError as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[E]{Style.RESET_ALL} Render error: {e}")
        sys.exit(1)

    print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Saved: {out_path}")


if __name__ == "__main__":
    main()
