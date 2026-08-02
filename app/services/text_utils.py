import re

BOILERPLATE_PATTERNS = [
    r"(?i)equal opportunity employer.*?(?=\n\n|\Z)",
    r"(?i)about (the company|us)[:\-].*?(?=\n\n|\Z)",
    r"(?i)we are committed to diversity.*?(?=\n\n|\Z)",
    r"(?i)benefits (include|package).*?(?=\n\n|\Z)",
]


def clean_jd(jd_text: str, max_words: int = 600) -> str:
    cleaned = jd_text
    for pattern in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    words = cleaned.split()
    if len(words) > max_words:
        cleaned = " ".join(words[:max_words])
    return cleaned


def truncate_section(text: str, max_words: int = 400) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."
