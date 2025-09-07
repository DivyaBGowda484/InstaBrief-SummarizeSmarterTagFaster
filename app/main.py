from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from config.settings import settings
from app.routes.auth import router as auth_router
from app.routes.articles import router as articles_router
from app.routes.summarize import router as summarize_router
from app.routes.feedback import router as feedback_router
from app.routes.users import router as users_router
from app.routes.tags import router as tags_router

app = FastAPI(title="InstaBrief API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(articles_router, prefix="/api/articles", tags=["articles"])
app.include_router(summarize_router, prefix="/api/summarize", tags=["summarize"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tags_router, prefix="/api/tags", tags=["tags"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def serve_frontend():
    """Serve the frontend application"""
    return FileResponse("frontend/index.html")


@app.get("/docs")
async def serve_docs():
    """Serve API documentation"""
    return FileResponse("frontend/index.html")
