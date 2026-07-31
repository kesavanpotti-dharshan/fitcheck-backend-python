from fastapi import APIRouter, UploadFile
from app.services.resume_parser import extract_text, chunk_by_section
from app.services.embeddings import embed_text
import uuid

router = APIRouter()

# In-memory store for now — swap for pgvector later
RESUME_STORE: dict[str, dict] = {}


@router.post("/upload")
async def upload_resume(file: UploadFile):
    raw_bytes = await file.read()
    text = extract_text(raw_bytes)
    print("Extracted text:" + text)
    sections = chunk_by_section(text)
    print("Sections:-" + str(sections))

    embedded_sections = {
        section: {"text": content, "embedding": embed_text(content)}
        for section, content in sections.items()
    }

    resume_id = str(uuid.uuid4())
    RESUME_STORE[resume_id] = embedded_sections

    return {"resume_id": resume_id, "sections": list(sections.keys())}
