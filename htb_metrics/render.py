from __future__ import annotations
import asyncio
import re
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates" / "html"
SVG_TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates" / "svg"


class TemplateNotFoundError(FileNotFoundError):
    pass


def inject(template: str, data: dict[str, Any], hide_if_null: bool) -> str:
    def _replace(m: re.Match) -> str:
        val = data.get(m.group(1))
        if val is None:
            return "" if hide_if_null else m.group(0)
        return str(val)

    return re.sub(r"\$(\w+)\$", _replace, template)


# ── HTML templates ────────────────────────────────────────────────────────────

async def _screenshot_html(html_path: Path, png_path: Path) -> None:
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

    rendered = inject(template_path.read_text(), data, hide_if_null)
    html_out = out / f"htb-metrics.{template_name}.html"
    html_out.write_text(rendered)

    png_out = out / f"htb-metrics.{template_name}.png"
    asyncio.run(_screenshot_html(html_out, png_out))

    return png_out


# ── SVG templates ─────────────────────────────────────────────────────────────

async def _screenshot_svg(svg_path: Path, png_path: Path) -> None:
    from playwright.async_api import async_playwright

    content = svg_path.read_text()
    m = re.search(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', content)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (480, 400)

    # Wrap in HTML — disable CSS animations so all content is immediately visible
    no_anim = (
        "*,*::before,*::after{"
        "animation-duration:0s!important;"
        "animation-delay:0s!important;"
        "transition-duration:0s!important}"
        ".stdin{width:100%!important}"
        ".stdout{max-height:none!important}"
        "footer{width:100%!important}"
    )
    wrapper = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
        f"<style>*{{margin:0;padding:0}}body{{background:transparent}}{no_anim}</style>"
        f"</head><body>{content}</body></html>"
    )
    tmp = svg_path.with_suffix(".screenshot.html")
    tmp.write_text(wrapper)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": w, "height": h})
            await page.goto(f"file://{tmp.resolve()}", wait_until="networkidle")
            await page.screenshot(
                path=str(png_path),
                type="png",
                clip={"x": 0, "y": 0, "width": w, "height": h},
            )
            await browser.close()
    finally:
        tmp.unlink(missing_ok=True)


def render_svg(
    template_name: str,
    data: dict[str, Any],
    output_dir: str,
    hide_if_null: bool = True,
) -> tuple[Path, Path]:
    template_path = SVG_TEMPLATES_DIR / f"{template_name}.svg"
    if not template_path.exists():
        raise TemplateNotFoundError(f"SVG template not found: {template_path}")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    rendered = inject(template_path.read_text(), data, hide_if_null)
    svg_out = out / f"htb-metrics.{template_name}.svg"
    svg_out.write_text(rendered)

    png_out = out / f"htb-metrics.{template_name}.png"
    asyncio.run(_screenshot_svg(svg_out, png_out))

    return svg_out, png_out
