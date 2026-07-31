from fastapi import FastAPI
from app.routers import resume, analyze

app = FastAPI(title="JD-Resume Gap Analyzer")

app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])


@app.get("/health")
def health():
    return {"status": "ok"}
