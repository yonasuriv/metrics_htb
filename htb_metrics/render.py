from __future__ import annotations
import asyncio
import re
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"


class TemplateNotFoundError(FileNotFoundError):
    pass


def inject(template_html: str, data: dict[str, Any], hide_if_null: bool) -> str:
    def _replace(m: re.Match) -> str:
        val = data.get(m.group(1))
        if val is None:
            return "" if hide_if_null else m.group(0)
        return str(val)

    return re.sub(r"\$(\w+)\$", _replace, template_html)


async def _screenshot(html_path: Path, png_path: Path) -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        element = await page.query_selector(".badge")
        if element is None:
            await browser.close()
            raise RuntimeError(f"No .badge element found in {html_path.name}")
        await element.screenshot(path=str(png_path), type="png")
        await browser.close()


def render(
    template_name: str,
    data: dict[str, Any],
    output_dir: str,
    hide_if_null: bool = True,
) -> Path:
    template_path = TEMPLATES_DIR / f"{template_name}.html"
    if not template_path.exists():
        raise TemplateNotFoundError(f"Template not found: {template_path}")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    rendered_html = inject(template_path.read_text(), data, hide_if_null)
    html_out = out / f"htb-metrics.{template_name}.html"
    html_out.write_text(rendered_html)

    png_out = out / f"htb-metrics.{template_name}.png"
    asyncio.run(_screenshot(html_out, png_out))

    return png_out
