"""LLM auto-formatting module for cvbuilder.

Uses llmdog to convert raw text/JSON input into structured Markdown resume format.
"""

from llmdog import chat
from larkfunc import clean_llm_response,parse_json_safely


PROMPT_ZH = """你是一个专业的简历格式化助手。请将以下原始简历信息整理为标准的 Markdown 简历格式。

要求：
1. 使用中文输出
2. 第一行为 `# 姓名`（一级标题）
3. 紧跟联系信息（邮箱、电话、地址等，使用一行文本，用 | 分隔）
4. 使用 `## 二级标题` 划分各节（如：教育背景、工作经历、项目经验、专业技能等）
5. 教育背景和工作经历使用 `### 三级标题` 标注，并将时间段放在同一行右对齐，格式为：
   `### <div class="edu-row"><strong>学校/公司名称 - 学位/职位</strong> <span>时间段</span></div>`
6. 使用无序列表 `-` 描述具体内容
7. 确保格式整洁、专业、适合生成 PDF
8. 只输出 Markdown 内容，不要添加任何解释

原始简历信息：
{content}
"""

PROMPT_EN = """You are a professional resume formatting assistant. Please convert the following raw resume information into a well-structured Markdown resume format.

Requirements:
1. Output in English
2. First line should be `# Full Name` (h1 heading)
3. Followed by contact info (email, phone, location, etc., in one line separated by |)
4. Use `## Section Title` for major sections (e.g., Education, Experience, Projects, Skills)
5. For Education and Experience entries, use `###` heading with time period on the same line, right-aligned:
   `### <div class="edu-row"><strong>School/Company - Degree/Position</strong> <span>Time Period</span></div>`
6. Use bullet points `-` for descriptions
7. Ensure the format is clean, professional, and suitable for PDF generation
8. Only output Markdown content, no explanations

Raw resume information:
{content}
"""


def format_resume(input_text: str, lang: str = "auto", verbose: bool = False) -> str:
    """Format raw text/JSON input into structured Markdown resume using LLM.

    Args:
        input_text: Raw resume content (text or JSON string).
        lang: Target language ('zh', 'en', or 'auto').
              If 'auto', will be determined by input content.
        verbose: If True, print LLM configuration info.

    Returns:
        Formatted Markdown resume text.

    Raises:
        RuntimeError: If LLM call fails or returns empty response.
    """
    from cvbuilder.lang_detect import detect_language

    # Determine target language
    if lang == "auto":
        lang = detect_language(input_text)

    # Load and display LLM configuration
    if verbose:
        from llmdog.config import load_config
        from rich.console import Console
        
        console = Console()
        cfg = load_config()
        
        console.print("\n[bold cyan]📋 LLM 配置信息:[/bold cyan]")
        console.print(f"  API 端点: [yellow]{cfg.api_url}[/yellow]")
        console.print(f"  模型名称: [yellow]{cfg.model}[/yellow]")
        console.print(f"  超时时间: [yellow]{cfg.timeout}秒[/yellow]")
        console.print(f"  最大重试: [yellow]{cfg.max_retries}次[/yellow]")
        console.print(f"  后端类型: [yellow]{cfg.backend or '默认'}[/yellow]")
        console.print(f"  目标语言: [yellow]{'中文' if lang == 'zh' else 'English'}[/yellow]")
        console.print()

    # Select prompt template
    prompt_template = PROMPT_ZH if lang == "zh" else PROMPT_EN
    prompt = prompt_template.format(content=input_text)

    # Call LLM via llmdog
    reply = chat(prompt)

    if not reply or not reply.strip():
        raise RuntimeError("LLM 返回空响应，请检查 llmdog 配置是否正确。")

    # Clean LLM response (remove code block markers etc.)
    cleaned = clean_llm_response(reply)


    return cleaned
