from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    resume_id: str
    job_description: str


class GapItem(BaseModel):
    requirement: str
    match_status: str  # "match" | "partial" | "missing"
    evidence: str | None = None
    suggestion: str | None = None
