from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from collections import Counter

from app.routes.auth import get_current_user
from config.db import get_database

router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
async def list_tags(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get most popular tags for the current user"""
    db = await get_database()
    
    pipeline = [
        {"$match": {"user_id": current_user["id"]}},
        {"$unwind": {"path": "$tags", "preserveNullAndEmptyArrays": False}},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    
    tags = []
    async for row in db.documents.aggregate(pipeline):
        tags.append({"tag": row["_id"], "count": row["count"]})
    
    return tags


@router.get("/suggest", response_model=List[str])
async def suggest_tags(
    query: str = Query("", description="Search query for tags"),
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user)
):
    """Get tag suggestions based on query"""
    db = await get_database()
    
    # Get all tags from user's documents
    pipeline = [
        {"$match": {"user_id": current_user["id"]}},
        {"$unwind": {"path": "$tags", "preserveNullAndEmptyArrays": False}},
        {"$group": {"_id": "$tags"}},
        {"$sort": {"_id": 1}}
    ]
    
    all_tags = set()
    async for row in db.documents.aggregate(pipeline):
        all_tags.add(row["_id"])
    
    # Filter tags based on query
    if query:
        suggestions = [tag for tag in all_tags if query.lower() in tag.lower()]
    else:
        suggestions = list(all_tags)
    
    return suggestions[:limit]


@router.get("/stats", response_model=Dict[str, Any])
async def get_tag_stats(current_user: dict = Depends(get_current_user)):
    """Get tag statistics for the current user"""
    db = await get_database()
    
    # Get all tags with counts
    pipeline = [
        {"$match": {"user_id": current_user["id"]}},
        {"$unwind": {"path": "$tags", "preserveNullAndEmptyArrays": False}},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    tag_counts = {}
    async for row in db.documents.aggregate(pipeline):
        tag_counts[row["_id"]] = row["count"]
    
    total_tags = len(tag_counts)
    total_usage = sum(tag_counts.values())
    most_used = max(tag_counts.items(), key=lambda x: x[1]) if tag_counts else ("", 0)
    
    return {
        "total_unique_tags": total_tags,
        "total_tag_usage": total_usage,
        "most_used_tag": most_used[0],
        "most_used_count": most_used[1],
        "average_usage_per_tag": total_usage / total_tags if total_tags > 0 else 0
    }
