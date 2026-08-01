from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest
from app.services.embeddings import embed_text
from app.services.retrieval import retrieve_top_sections
from app.services.gemini_client import analyze_gaps
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

    jd_embedding = embed_text(payload.job_description)
    top_sections = retrieve_top_sections(jd_embedding, resume_sections, top_k=3)

    gaps = analyze_gaps(payload.job_description, top_sections)

    return {"resume_id": payload.resume_id, "gaps": gaps}
