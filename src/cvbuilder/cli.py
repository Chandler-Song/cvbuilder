"""CLI entry point using Typer for cvbuilder."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from cvbuilder import __version__
from cvbuilder.config import (
    BUILTIN_STYLES,
    DEFAULTS,
    get_template_md_path,
    resolve_css_path,
)

app = typer.Typer(
    name="cvbuilder",
    help="Generate PDF resumes from Markdown with customizable styles and LLM formatting.",
)
console = Console()

LLMDOG_YAML_EXAMPLE = """# llmdog 配置文件
# 将此文件复制为 .llmdog.yaml 并填入真实配置
api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
api_url: https://api.deepseek.com/v1/chat/completions
model: deepseek-chat
timeout: 60
verify_ssl: true
"""


@app.callback(invoke_without_command=True)
def _version_callback(
    version: bool = typer.Option(  # noqa: B008
        False, "--version", "-v", help="显示版本号并退出。"
    ),
) -> None:
    if version:
        typer.echo(f"cvbuilder {__version__}")
        raise typer.Exit()


@app.command(help="初始化简历模板文件到当前目录。")
def init(
    lang: str = typer.Option(  # noqa: B008
        "all", help="语言: zh（中文）、en（英文）或 all（全部）。"
    ),
    force: bool = typer.Option(  # noqa: B008
        False, "--force", "-f", help="强制覆盖已存在的文件。"
    ),
) -> None:
    """Initialize resume templates in the current directory."""
    from cvbuilder.config import get_style_path

    created_files: list[str] = []
    skipped_files: list[str] = []

    # Determine which MD templates to copy
    if lang == "all":
        md_langs = ["zh", "en"]
    elif lang in ("zh", "en"):
        md_langs = [lang]
    else:
        console.print(
            f"[red]错误: 不支持的语言 '{lang}'，请使用 'zh'、'en' 或 'all'。[/red]"
        )
        raise typer.Exit(code=1)

    # Copy MD templates
    for md_lang in md_langs:
        md_src = get_template_md_path(md_lang)
        if md_src is None:
            console.print(f"[red]错误: 找不到 {md_lang} 模板文件。[/red]")
            continue

        if md_lang == "zh":
            md_dst = Path("resume_zh.md")
        else:
            md_dst = Path("resume_en.md")

        if md_dst.exists() and not force:
            skipped_files.append(str(md_dst))
        else:
            md_dst.write_text(md_src.read_text(encoding="utf-8"), encoding="utf-8")
            created_files.append(str(md_dst))

    # Copy all CSS styles
    for style_name in BUILTIN_STYLES:
        css_src = get_style_path(style_name)
        if css_src is None:
            console.print(f"[yellow]警告: 找不到 {style_name} 样式文件。[/yellow]")
            continue

        css_dst = Path(f"{style_name}.css")
        if css_dst.exists() and not force:
            skipped_files.append(str(css_dst))
        else:
            css_dst.write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")
            created_files.append(str(css_dst))

    # Display results
    if created_files:
        console.print("\n[green]✓ 已创建以下文件:[/green]")
        for f in created_files:
            console.print(f"  [green]• {f}[/green]")

    if skipped_files:
        console.print("\n[yellow]⊘ 已跳过以下文件（已存在）:[/yellow]")
        for f in skipped_files:
            console.print(f"  [yellow]• {f}[/yellow]")
        console.print("\n[dim]使用 --force 或 -f 参数强制覆盖[/dim]")

    console.print("\n[bold]下一步：[/bold]")
    console.print("  1. 编辑模板文件，填入你的简历内容")
    console.print("  2. 选择样式：cvbuilder styles 查看所有可用样式")
    console.print("  3. 生成 PDF：cvbuilder build --md <模板文件> --css <样式文件>")


@app.command(help="从 Markdown 生成 PDF 简历（已格式化内容直接转换）。")
def build(
    md: Path = typer.Option(  # noqa: B008
        Path(str(DEFAULTS["md"])), help="Markdown 文件路径。"
    ),
    css: str = typer.Option(  # noqa: B008
        str(DEFAULTS["css"]), help="内置样式名称或自定义 CSS 文件路径。"
    ),
    output: Path = typer.Option(  # noqa: B008
        None, help="输出 PDF 路径（默认与 md 文件同名 .pdf）。"
    ),
    lang: str = typer.Option(  # noqa: B008
        "auto", help="语言: zh / en / auto（自动检测）。"
    ),
    header: str = typer.Option(  # noqa: B008
        None, "--header", help="页眉文字内容。"
    ),
    header_image: str = typer.Option(  # noqa: B008
        None, "--header-image", help="页眉图片文件路径。"
    ),
    footer: str = typer.Option(  # noqa: B008
        None, "--footer", help="页脚文字内容。"
    ),
    footer_image: str = typer.Option(  # noqa: B008
        None, "--footer-image", help="页脚图片文件路径。"
    ),
    no_html: bool = typer.Option(  # noqa: B008
        False, "--no-html", help="不生成中间 HTML 文件。"
    ),
) -> None:
    """Build PDF from formatted Markdown resume."""
    # Validate markdown file
    if not md.is_file():
        console.print(f"[red]错误: Markdown 文件不存在: {md}[/red]")
        raise typer.Exit(code=1)

    # Resolve CSS
    resolved_css = resolve_css_path(css)
    if resolved_css is None:
        console.print(f"[red]错误: 找不到 CSS 样式: {css}[/red]")
        console.print(
            f"[dim]可用内置样式: {', '.join(BUILTIN_STYLES)}[/dim]"
        )
        raise typer.Exit(code=1)

    # Determine output path
    if output is None:
        output = md.with_suffix(".pdf")

    # Check Playwright browser
    from cvbuilder.converter import check_playwright_browser

    if not check_playwright_browser():
        console.print(
            "[red]错误: Playwright Chromium 未安装。[/red]\n"
            "[dim]请运行: playwright install chromium[/dim]"
        )
        raise typer.Exit(code=1)

    # Generate PDF
    from cvbuilder.converter import convert

    console.print(f"[dim]正在生成 PDF...[/dim]")
    convert(
        md_path=md,
        css_path=resolved_css,
        output=output,
        lang=lang,
        header_text=header,
        header_image=header_image,
        footer_text=footer,
        footer_image=footer_image,
    )
    console.print(f"[green]✓ 已生成: {output}[/green]")

    # Optionally generate HTML
    if not no_html:
        html_output = output.with_suffix(".html")
        md_text = md.read_text(encoding="utf-8")
        css_text = resolved_css.read_text(encoding="utf-8")

        from cvbuilder.html_builder import build_header_html, build_footer_html, build_html
        from cvbuilder.lang_detect import detect_language

        detected_lang = lang if lang != "auto" else detect_language(md_text)
        header_html = build_header_html(text=header, image_path=header_image)
        footer_html = build_footer_html(text=footer, image_path=footer_image)
        html_content = build_html(
            md_text=md_text,
            css_text=css_text,
            lang=detected_lang,
            header_html=header_html,
            footer_html=footer_html,
        )
        html_output.write_text(html_content, encoding="utf-8")
        console.print(f"[green]✓ 已生成: {html_output}[/green]")


@app.command(help="使用 LLM 自动格式化原始简历并生成 PDF。")
def format(
    input: Path = typer.Option(  # noqa: B008
        ..., "--input", "-i", help="输入文件路径（txt 或 json）。"
    ),
    output: Path = typer.Option(  # noqa: B008
        None, "--output", "-o", help="输出 PDF 路径（默认与输入文件同名 .pdf）。"
    ),
    css: str = typer.Option(  # noqa: B008
        str(DEFAULTS["css"]), help="内置样式名称或自定义 CSS 文件路径。"
    ),
    lang: str = typer.Option(  # noqa: B008
        "auto", help="目标语言: zh / en / auto（自动检测）。"
    ),
    header: str = typer.Option(  # noqa: B008
        None, "--header", help="页眉文字内容。"
    ),
    header_image: str = typer.Option(  # noqa: B008
        None, "--header-image", help="页眉图片文件路径。"
    ),
    footer: str = typer.Option(  # noqa: B008
        None, "--footer", help="页脚文字内容。"
    ),
    footer_image: str = typer.Option(  # noqa: B008
        None, "--footer-image", help="页脚图片文件路径。"
    ),
    md_only: bool = typer.Option(  # noqa: B008
        False, "--md-only", help="只输出 Markdown 文件，不生成 PDF。"
    ),
    verbose: bool = typer.Option(  # noqa: B008
        False, "--verbose", "-v", help="显示 LLM 配置信息。"
    ),
) -> None:
    """Format raw text/JSON input using LLM and generate PDF."""
    # Validate input file
    if not input.is_file():
        console.print(f"[red]错误: 输入文件不存在: {input}[/red]")
        raise typer.Exit(code=1)

    # Read input
    input_text = input.read_text(encoding="utf-8")

    # Format with LLM
    console.print("[dim]正在使用 LLM 格式化简历...[/dim]")
    try:
        from cvbuilder.formatter import format_resume

        md_text = format_resume(input_text=input_text, lang=lang, verbose=verbose)
    except RuntimeError as e:
        console.print(f"[red]错误: {e}[/red]")
        raise typer.Exit(code=1) from None

    console.print("[green]✓ LLM 格式化完成[/green]")

    # Determine output paths
    if output is None:
        if md_only:
            output = input.with_suffix(".md")
        else:
            output = input.with_suffix(".pdf")

    # Save Markdown file
    md_output = output.with_suffix(".md") if not md_only else output
    md_output.write_text(md_text, encoding="utf-8")
    console.print(f"[green]✓ 已保存格式化 Markdown: {md_output}[/green]")

    # If md_only mode, skip PDF generation
    if md_only:
        console.print("\n[dim]提示: 使用 --md-only 模式，未生成 PDF[/dim]")
        console.print("[dim]如需生成 PDF，运行: cvbuilder build --md {}[/dim]".format(md_output))
        return

    # Resolve CSS
    resolved_css = resolve_css_path(css)
    if resolved_css is None:
        console.print(f"[red]错误: 找不到 CSS 样式: {css}[/red]")
        raise typer.Exit(code=1)

    # Check Playwright
    from cvbuilder.converter import check_playwright_browser

    if not check_playwright_browser():
        console.print(
            "[red]错误: Playwright Chromium 未安装。[/red]\n"
            "[dim]请运行: playwright install chromium[/dim]"
        )
        raise typer.Exit(code=1)

    # Generate PDF from formatted markdown
    console.print("[dim]正在生成 PDF...[/dim]")
    from cvbuilder.converter import convert_from_text

    convert_from_text(
        md_text=md_text,
        css_path=resolved_css,
        output=output,
        lang=lang,
        header_text=header,
        header_image=header_image,
        footer_text=footer,
        footer_image=footer_image,
    )
    console.print(f"[green]✓ 已生成: {output}[/green]")


@app.command(help="列出所有可用的内置 CSS 样式。")
def styles() -> None:
    """List all available built-in CSS styles."""
    table = Table(title="可用内置样式")
    table.add_column("样式名称", style="cyan")
    table.add_column("说明")

    style_descriptions = {
        "default": "默认样式 - 中英文通用，专业简洁",
        "modern": "现代风格 - 大留白、简约分隔、强调色",
        "classic": "经典风格 - 传统正式、衬线字体、保守配色",
        "elegant": "优雅风格 - 渐变强调色、卡片式区块、柔和视觉层次",
    }

    for style_name in BUILTIN_STYLES:
        desc = style_descriptions.get(style_name, "")
        table.add_row(style_name, desc)

    console.print(table)
    console.print("\n[dim]使用方法: cvbuilder build --css <样式名>[/dim]")


@app.command("llm-config", help="生成 llmdog 配置文件示例并打印配置指引。")
def llm_config() -> None:
    """Generate .llmdog.yaml.example and print configuration guide."""
    example_path = Path(".llmdog.yaml.example")
    example_path.write_text(LLMDOG_YAML_EXAMPLE, encoding="utf-8")
    console.print(
        f"[green]✓ 已生成示例配置文件: [cyan]{example_path}[/cyan][/green]"
    )

    console.print("\n[bold]配置步骤：[/bold]")
    console.print("  1. 复制示例文件：cp .llmdog.yaml.example .llmdog.yaml")
    console.print("  2. 编辑 .llmdog.yaml，填入你的真实 API Key 和模型配置")
    console.print("  3. 确保 .llmdog.yaml 已加入 .gitignore（避免泄露密钥）")
    console.print("\n[bold]配置文件查找顺序：[/bold]")
    console.print(
        "  优先级：项目根目录 .llmdog.yaml > 家目录 ~/.llmdog.yaml > .env > 默认配置"
    )
    console.print("\nℹ 详细文档请参考 llmdog 官方说明", style="cyan")


if __name__ == "__main__":
    app()
