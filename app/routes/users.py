from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from app.models.schemas import UserPublic, DocumentPublic
from app.routes.auth import get_current_user
from config.db import get_database

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserPublic(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        role=current_user.get("role", "user"),
        created_at=current_user["created_at"],
        is_active=current_user.get("is_active", True)
    )


@router.get("/me/documents", response_model=List[DocumentPublic])
async def get_user_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get current user's documents"""
    db = await get_database()
    
    cursor = db.documents.find({"user_id": current_user["id"]}).skip(skip).limit(limit)
    documents = []
    
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        documents.append(DocumentPublic(**doc))
    
    return documents


@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    db = await get_database()
    
    # Count documents
    total_documents = await db.documents.count_documents({"user_id": current_user["id"]})
    
    # Count summaries
    total_summaries = await db.documents.count_documents({
        "user_id": current_user["id"],
        "summary": {"$exists": True, "$ne": ""}
    })
    
    # Count feedback
    total_feedback = await db.feedback.count_documents({"user_id": current_user["id"]})
    
    return {
        "total_documents": total_documents,
        "total_summaries": total_summaries,
        "total_feedback": total_feedback,
        "account_created": current_user["created_at"].isoformat() if current_user.get("created_at") else None
    }
