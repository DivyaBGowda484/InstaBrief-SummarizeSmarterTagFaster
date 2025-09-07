from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId

from app.models.schemas import FeedbackCreate, FeedbackPublic
from app.routes.auth import get_current_user
from config.db import get_database

router = APIRouter()


@router.post("/", response_model=FeedbackPublic)
async def submit_feedback(
    feedback: FeedbackCreate,
    current_user: dict = Depends(get_current_user)
):
    """Submit feedback for a document"""
    db = await get_database()
    
    # Verify document exists and belongs to user
    doc = await db.documents.find_one({
        "_id": ObjectId(feedback.document_id),
        "user_id": current_user["id"]
    })
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Create feedback document
    feedback_doc = {
        "document_id": feedback.document_id,
        "user_id": current_user["id"],
        "helpful": feedback.helpful,
        "rating": feedback.rating,
        "comments": feedback.comments,
        "summary_quality": feedback.summary_quality,
        "tag_accuracy": feedback.tag_accuracy,
        "created_at": datetime.utcnow()
    }
    
    result = await db.feedback.insert_one(feedback_doc)
    
    return FeedbackPublic(
        id=str(result.inserted_id),
        document_id=feedback.document_id,
        helpful=feedback.helpful,
        rating=feedback.rating,
        comments=feedback.comments,
        summary_quality=feedback.summary_quality,
        tag_accuracy=feedback.tag_accuracy,
        created_at=feedback_doc["created_at"],
        user_id=current_user["id"]
    )


@router.get("/", response_model=List[FeedbackPublic])
async def get_feedback(
    document_id: str = None,
    current_user: dict = Depends(get_current_user)
):
    """Get feedback for documents"""
    db = await get_database()
    
    query = {"user_id": current_user["id"]}
    if document_id:
        query["document_id"] = document_id
    
    cursor = db.feedback.find(query).sort("created_at", -1)
    feedback_list = []
    
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        feedback_list.append(FeedbackPublic(**doc))
    
    return feedback_list
