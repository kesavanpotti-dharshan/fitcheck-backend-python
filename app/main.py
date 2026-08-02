from fastapi import FastAPI
from app.routers import resume, analyze
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FitCheck-Resume Gap Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fitcheck-resume.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])


@app.get("/health")
def health():
    return {"status": "ok"}
