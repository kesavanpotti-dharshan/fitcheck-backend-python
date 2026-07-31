from pypdf import PdfReader
import io


def extract_text(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_by_section(text: str) -> dict[str, str]:
    """Naive section splitter — looks for common resume headers."""
    headers = ["experience", "education", "skills", "projects", "summary"]
    sections: dict[str, str] = {}
    current = "summary"
    sections[current] = ""

    for line in text.split("\n"):
        stripped = line.strip().lower()
        matched = next((h for h in headers if stripped.startswith(h)), None)
        if matched:
            current = matched
            sections[current] = ""
        else:
            sections[current] += line + "\n"

    return {k: v.strip() for k, v in sections.items() if v.strip()}
