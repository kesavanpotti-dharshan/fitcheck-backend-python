from fastapi import APIRouter
from app.models.schemas import AnalyzeRequest

router = APIRouter()


@router.post("/")
async def analyze_gap(payload: AnalyzeRequest):
    # TODO: retrieve chunks, call Gemini, return structured gaps
    return {"resume_id": payload.resume_id, "gaps": []}
