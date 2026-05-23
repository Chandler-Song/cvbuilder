"""Language detection module for cvbuilder."""

import re


def detect_language(text: str) -> str:
    """Detect the primary language of text content.

    Uses Unicode character ranges to determine if the text is primarily
    Chinese (CJK) or English.

    Args:
        text: Input text to analyze.

    Returns:
        "zh" if Chinese characters are detected above threshold, "en" otherwise.
    """
    if not text.strip():
        return "en"

    # Count CJK characters (CJK Unified Ideographs range)
    cjk_pattern = re.compile(
        r"[\u4e00-\u9fff"  # CJK Unified Ideographs
        r"\u3400-\u4dbf"  # CJK Unified Ideographs Extension A
        r"\u2e80-\u2eff"  # CJK Radicals Supplement
        r"\u3000-\u303f"  # CJK Symbols and Punctuation
        r"\uff00-\uffef]"  # Fullwidth Forms
    )

    cjk_chars = len(cjk_pattern.findall(text))

    # Count total non-whitespace characters
    total_chars = len(re.sub(r"\s", "", text))

    if total_chars == 0:
        return "en"

    # If CJK characters make up more than 5% of text, consider it Chinese
    cjk_ratio = cjk_chars / total_chars
    return "zh" if cjk_ratio > 0.05 else "en"
