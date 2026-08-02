from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest
from app.services.embeddings import embed_text
from app.services.retrieval import retrieve_top_sections
from app.services.gemini_client import analyze_gaps
from app.services.text_utils import clean_jd, truncate_section
from app.routers.resume import RESUME_STORE
from app.utils.sanitized_route import SanitizedRoute

router = APIRouter(route_class=SanitizedRoute)


@router.post("/")
async def analyze_gap(payload: AnalyzeRequest):
    resume_sections = RESUME_STORE.get(payload.resume_id)
    if not resume_sections:
        raise HTTPException(
            status_code=404, detail="Resume not found. Upload it first."
        )

    jd_cleaned = clean_jd(payload.job_description)
    jd_embedding = embed_text(jd_cleaned)
    top_sections = retrieve_top_sections(jd_embedding, resume_sections, top_k=3)

    for section in top_sections:
        section["text"] = truncate_section(section["text"])

    gaps, usage = analyze_gaps(jd_cleaned, top_sections)

    return {"resume_id": payload.resume_id, "gaps": gaps, "usage": usage}
