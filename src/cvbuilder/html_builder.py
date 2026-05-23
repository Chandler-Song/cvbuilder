"""Build complete HTML documents from Markdown and CSS for cvbuilder."""

import base64
from pathlib import Path

import markdown


def _encode_image_to_base64(image_path: str) -> str:
    """Read an image file and return its base64-encoded data URI.

    Args:
        image_path: Path to the image file.

    Returns:
        Base64 data URI string for embedding in HTML.
    """
    path = Path(image_path)
    if not path.is_file():
        return ""

    suffix = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{data}"


def build_header_html(
    text: str | None = None,
    image_path: str | None = None,
) -> str:
    """Build header HTML fragment.

    Args:
        text: Header text content.
        image_path: Path to header image file.

    Returns:
        HTML string for header section, or empty string if no content.
    """
    if not text and not image_path:
        return ""

    parts: list[str] = []
    if image_path:
        data_uri = _encode_image_to_base64(image_path)
        if data_uri:
            parts.append(
                f'<img src="{data_uri}" class="header-image" '
                f'alt="header" style="max-height: 40px;" />'
            )
    if text:
        parts.append(f'<span class="header-text">{text}</span>')

    content = " ".join(parts)
    return f'<header class="page-header">{content}</header>'


def build_footer_html(
    text: str | None = None,
    image_path: str | None = None,
) -> str:
    """Build footer HTML fragment.

    Args:
        text: Footer text content.
        image_path: Path to footer image file.

    Returns:
        HTML string for footer section, or empty string if no content.
    """
    if not text and not image_path:
        return ""

    parts: list[str] = []
    if image_path:
        data_uri = _encode_image_to_base64(image_path)
        if data_uri:
            parts.append(
                f'<img src="{data_uri}" class="footer-image" '
                f'alt="footer" style="max-height: 30px;" />'
            )
    if text:
        parts.append(f'<span class="footer-text">{text}</span>')

    content = " ".join(parts)
    return f'<footer class="page-footer">{content}</footer>'


def build_html(
    md_text: str,
    css_text: str,
    lang: str = "en",
    header_html: str = "",
    footer_html: str = "",
) -> str:
    """Convert Markdown text to a complete HTML document with embedded CSS.

    Args:
        md_text: Markdown content to convert.
        css_text: CSS stylesheet content.
        lang: Language code for html lang attribute ('zh' or 'en').
        header_html: HTML fragment for page header.
        footer_html: HTML fragment for page footer.

    Returns:
        Complete HTML document string.
    """
    # Convert markdown to HTML body
    body_html = markdown.markdown(
        md_text,
        extensions=["extra", "smarty", "sane_lists"],
    )

    # Map language code to HTML lang attribute
    lang_attr = "zh-CN" if lang == "zh" else "en"

    # Build header/footer CSS
    header_footer_css = """
    .page-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        padding: 5mm 10mm;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 10px;
        color: #666;
    }
    .page-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 5mm 10mm;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 10px;
        color: #666;
    }
    .page-header .header-image,
    .page-footer .footer-image {
        vertical-align: middle;
    }
"""

    # Only include header/footer CSS if needed
    extra_css = header_footer_css if (header_html or footer_html) else ""

    return (
        "<!doctype html>\n"
        f'<html lang="{lang_attr}">\n'
        "  <head>\n"
        '    <meta charset="utf-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        "    <style>\n"
        f"{css_text}\n"
        f"{extra_css}\n"
        "    </style>\n"
        "  </head>\n"
        "  <body>\n"
        f"    {header_html}\n"
        f'    <div id="write">{body_html}</div>\n'
        f"    {footer_html}\n"
        "  </body>\n"
        "</html>\n"
    )
