#!/usr/bin/env python3
"""Download static HTB icons to assets/icons/ for local template use."""
import sys
from pathlib import Path
import requests

ICONS_DIR = Path(__file__).parent.parent / "assets" / "icons"
HTB_BASE = "https://app.hackthebox.com/images/icons"

ICONS = {
    "ic-userflag.svg":     f"{HTB_BASE}/ic-machines/ic-userflag.svg",
    "ic-rootflag.svg":     f"{HTB_BASE}/ic-machines/ic-rootflag.svg",
    "ic-userblood.svg":    f"{HTB_BASE}/ic-machines/ic-userblood.svg",
    "ic-rootblood.svg":    f"{HTB_BASE}/ic-machines/ic-rootblood.svg",
    "ic-points.svg":       f"{HTB_BASE}/ic-other/ic-points.svg",
    "ic-respect.svg":      f"{HTB_BASE}/ic-profile/ic-respect.svg",
    "ic-rank.svg":         f"{HTB_BASE}/ic-icons-kickass/ic-ranks-big2.svg",
    "ic-machines.svg":     f"{HTB_BASE}/ic-icons-kickass/ic-machines-big.svg",
    "ic-challenges.svg":   f"{HTB_BASE}/ic-icons-kickass/ic-challenges-big.svg",
    "ic-fortress.svg":     f"{HTB_BASE}/ic-icons-kickass/ic-fortress-big.svg",
}

def download():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in ICONS.items():
        dest = ICONS_DIR / filename
        if dest.exists():
            print(f"  skip (exists): {filename}")
            continue
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            content = resp.content
            if not (content.lstrip().startswith(b'<svg') or content.lstrip().startswith(b'<?xml')):
                print(f"  WARN: {filename} returned non-SVG content (likely auth-required URL), skipping", file=sys.stderr)
                continue
            dest.write_bytes(content)
            print(f"  downloaded: {filename}")
        else:
            print(f"  WARN: {resp.status_code} for {url}", file=sys.stderr)

if __name__ == "__main__":
    download()
