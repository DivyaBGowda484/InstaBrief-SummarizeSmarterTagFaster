from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

from config.settings import settings
from config.db import connect_to_mongo, connect_to_elasticsearch, close_mongo_connection, close_elasticsearch_connection
from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.summarize import router as summarize_router
from app.routes.feedback import router as feedback_router
from app.routes.users import router as users_router
from app.routes.tags import router as tags_router
from app.routes.search import router as search_router
from app.routes.analytics import router as analytics_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="InstaBrief API", 
    version="1.0.0",
    description="AI-powered document summarization and smart tagging platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])
app.include_router(summarize_router, prefix="/api/summarize", tags=["Summarization"])
app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(tags_router, prefix="/api/tags", tags=["Tags"])
app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])


@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup"""
    logger.info("Starting InstaBrief API...")
    await connect_to_mongo()
    await connect_to_elasticsearch()
    logger.info("InstaBrief API started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    logger.info("Shutting down InstaBrief API...")
    await close_mongo_connection()
    await close_elasticsearch_connection()
    logger.info("InstaBrief API shutdown complete!")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "InstaBrief API"
    }


@app.get("/")
async def serve_frontend():
    """Serve the frontend application"""
    return FileResponse("frontend/index.html")


@app.get("/docs")
async def serve_docs():
    """Serve API documentation"""
    return FileResponse("frontend/index.html")
