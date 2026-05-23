"""Convert Markdown to PDF via HTML and Playwright for cvbuilder."""

import asyncio
from pathlib import Path
from typing import cast

from pypdf import PdfReader

from cvbuilder.html_builder import build_header_html, build_footer_html, build_html
from cvbuilder.lang_detect import detect_language

MIN_SCALE = 0.55
MAX_SCALE = 1.0
DEFAULT_SCALE = 0.72
SCALE_STEP = 0.03
PAGE_WIDTH = 794
PAGE_HEIGHT = 1123
MARGIN_MM = 10


def check_playwright_browser() -> bool:
    """Check if Playwright Chromium browser is installed.

    Returns:
        True if Chromium is available, False otherwise.
    """
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            # Try to get executable path
            p.chromium.executable_path  # noqa: B018
        return True
    except Exception:
        return False


def convert(
    md_path: Path,
    css_path: Path,
    output: Path,
    lang: str = "auto",
    header_text: str | None = None,
    header_image: str | None = None,
    footer_text: str | None = None,
    footer_image: str | None = None,
) -> None:
    """Read MD and CSS files, generate PDF with optional header/footer.

    Args:
        md_path: Path to Markdown source file.
        css_path: Path to CSS stylesheet file.
        output: Output PDF file path.
        lang: Language code ('zh', 'en', or 'auto' for detection).
        header_text: Optional header text.
        header_image: Optional path to header image.
        footer_text: Optional footer text.
        footer_image: Optional path to footer image.
    """
    md_text = md_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")

    # Detect language if auto
    if lang == "auto":
        lang = detect_language(md_text)

    # Build header/footer HTML
    header_html = build_header_html(text=header_text, image_path=header_image)
    footer_html = build_footer_html(text=footer_text, image_path=footer_image)

    # Build full HTML
    html = build_html(
        md_text=md_text,
        css_text=css_text,
        lang=lang,
        header_html=header_html,
        footer_html=footer_html,
    )

    # Generate PDF
    _run_async_convert(html, output)


def convert_from_text(
    md_text: str,
    css_path: Path,
    output: Path,
    lang: str = "auto",
    header_text: str | None = None,
    header_image: str | None = None,
    footer_text: str | None = None,
    footer_image: str | None = None,
) -> None:
    """Convert Markdown text directly to PDF (used by format command).

    Args:
        md_text: Markdown content string.
        css_path: Path to CSS stylesheet file.
        output: Output PDF file path.
        lang: Language code ('zh', 'en', or 'auto' for detection).
        header_text: Optional header text.
        header_image: Optional path to header image.
        footer_text: Optional footer text.
        footer_image: Optional path to footer image.
    """
    css_text = css_path.read_text(encoding="utf-8")

    if lang == "auto":
        lang = detect_language(md_text)

    header_html = build_header_html(text=header_text, image_path=header_image)
    footer_html = build_footer_html(text=footer_text, image_path=footer_image)

    html = build_html(
        md_text=md_text,
        css_text=css_text,
        lang=lang,
        header_html=header_html,
        footer_html=footer_html,
    )

    _run_async_convert(html, output)


def _run_async_convert(html: str, output: Path) -> None:
    """Run the async PDF generation pipeline."""
    asyncio.run(_async_convert(html, output))


async def _async_convert(html: str, output: Path) -> None:
    """Generate PDF, with adaptive scaling to fit content."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        scale = await _measure_scale(browser, html)
        await _generate_pdf(browser, html, output, scale)

        pages = _count_pages(output)
        while pages > 1 and scale > MIN_SCALE:
            scale = round(max(MIN_SCALE, scale - SCALE_STEP), 3)
            await _generate_pdf(browser, html, output, scale)
            pages = _count_pages(output)

        await browser.close()


async def _measure_scale(browser: object, html: str) -> float:
    """Measure content height and calculate scale to fit page."""
    from playwright.async_api import Browser

    browser = cast(Browser, browser)
    page = await browser.new_page(
        viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT}
    )
    await page.set_content(html, wait_until="networkidle")
    await page.emulate_media(media="print")

    content_height = cast(
        float,
        await page.evaluate(
            """() => {
            const write = document.querySelector('#write');
            return write ? write.getBoundingClientRect().height : 0;
        }"""
        ),
    )
    await page.close()

    available_height = PAGE_HEIGHT - (MARGIN_MM / 25.4) * 96 * 2
    if content_height <= 0:
        return MAX_SCALE

    ratio = available_height / content_height
    return min(MAX_SCALE, max(DEFAULT_SCALE, ratio))


async def _generate_pdf(
    browser: object, html: str, output: Path, scale: float
) -> None:
    """Render HTML to PDF at the given scale."""
    from playwright.async_api import Browser

    browser = cast(Browser, browser)
    page = await browser.new_page(
        viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT}
    )
    await page.set_content(html, wait_until="networkidle")
    await page.emulate_media(media="print")

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    await page.pdf(
        path=str(output),
        format="A4",
        scale=scale,
        print_background=True,
        prefer_css_page_size=True,
        margin={
            "top": f"{MARGIN_MM}mm",
            "bottom": f"{MARGIN_MM}mm",
            "left": "12mm",
            "right": "12mm",
        },
    )
    await page.close()


def _count_pages(pdf_path: Path) -> int:
    """Count pages in a PDF file."""
    return len(PdfReader(str(pdf_path)).pages)
