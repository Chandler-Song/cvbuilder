"""Configuration and default values for cvbuilder."""

from pathlib import Path

TEMPLATES_DIR: Path = Path(__file__).parent / "templates"

# Built-in CSS style names
BUILTIN_STYLES: list[str] = ["default", "modern", "classic", "elegant"]

# Default configuration
DEFAULTS: dict[str, str | None] = {
    "md": "resume.md",
    "css": "default",
    "output": None,
    "lang": "auto",
}


def get_style_path(name: str) -> Path | None:
    """Return path to a built-in CSS style, or None if not found.

    Args:
        name: Name of built-in style (e.g. 'default', 'modern', 'classic')
              or a file path to a custom CSS file.

    Returns:
        Path to CSS file if found as built-in style, else None.
    """
    css_path = TEMPLATES_DIR / f"{name}.css"
    return css_path if css_path.is_file() else None


def get_template_md_path(lang: str) -> Path | None:
    """Return path to a built-in Markdown template for the given language.

    Args:
        lang: Language code ('zh' or 'en').

    Returns:
        Path to template file if found, else None.
    """
    if lang == "zh":
        md_path = TEMPLATES_DIR / "resume_zh.md"
    elif lang == "en":
        md_path = TEMPLATES_DIR / "resume_en.md"
    else:
        return None
    return md_path if md_path.is_file() else None


def resolve_css_path(css_arg: str) -> Path | None:
    """Resolve CSS argument to a valid file path.

    First checks if it's a built-in style name, then treats as file path.

    Args:
        css_arg: Built-in style name or path to CSS file.

    Returns:
        Resolved Path to CSS file, or None if not found.
    """
    # Check built-in styles first
    builtin = get_style_path(css_arg)
    if builtin is not None:
        return builtin

    # Treat as file path
    css_file = Path(css_arg)
    return css_file if css_file.is_file() else None
