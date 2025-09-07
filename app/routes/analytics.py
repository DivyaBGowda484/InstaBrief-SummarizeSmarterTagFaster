from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from typing import Dict, Any
from collections import Counter

from app.models.schemas import AnalyticsResponse
from app.routes.auth import get_current_user
from config.db import get_database

router = APIRouter()

@router.get("/", response_model=AnalyticsResponse)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Get user analytics and statistics"""
    
    db = await get_database()
    user_id = current_user["id"]
    
    # Get basic counts
    total_documents = await db.documents.count_documents({"user_id": user_id})
    total_summaries = await db.documents.count_documents({
        "user_id": user_id,
        "summary": {"$exists": True, "$ne": ""}
    })
    
    # Get all user documents for analysis
    documents_cursor = db.documents.find({"user_id": user_id})
    documents = []
    async for doc in documents_cursor:
        documents.append(doc)
    
    # Calculate time saved (estimate 5 minutes per document)
    time_saved_hours = total_documents * 5 / 60
    
    # Calculate efficiency gain (estimate 80% time reduction)
    efficiency_gain_percent = 80.0
    
    # Documents by type
    documents_by_type = {}
    for doc in documents:
        file_type = doc.get("file_type", "unknown")
        documents_by_type[file_type] = documents_by_type.get(file_type, 0) + 1
    
    # Recent activity (last 10 documents)
    recent_documents = sorted(
        documents, 
        key=lambda x: x.get("created_at", datetime.min), 
        reverse=True
    )[:10]
    
    # Convert to DocumentPublic format
    recent_activity = []
    for doc in recent_documents:
        doc["id"] = str(doc["_id"])
        recent_activity.append(doc)
    
    # Top tags
    all_tags = []
    for doc in documents:
        tags = doc.get("tags", [])
        all_tags.extend(tags)
    
    tag_counts = Counter(all_tags)
    top_tags = [
        {"tag": tag, "count": count} 
        for tag, count in tag_counts.most_common(10)
    ]
    
    # Processing stats
    processing_stats = {
        "total_processing_time": sum(
            doc.get("processing_time", 0) for doc in documents
        ),
        "average_processing_time": (
            sum(doc.get("processing_time", 0) for doc in documents) / len(documents)
            if documents else 0
        ),
        "algorithms_used": Counter(
            doc.get("algorithm_used", "unknown") for doc in documents
        ),
        "languages_detected": Counter(
            doc.get("language", "unknown") for doc in documents
        )
    }
    
    return AnalyticsResponse(
        total_documents=total_documents,
        total_summaries=total_summaries,
        total_tags=len(set(all_tags)),
        time_saved_hours=time_saved_hours,
        efficiency_gain_percent=efficiency_gain_percent,
        documents_by_type=documents_by_type,
        recent_activity=recent_activity,
        top_tags=top_tags,
        processing_stats=processing_stats
    )

@router.get("/charts")
async def get_chart_data(current_user: dict = Depends(get_current_user)):
    """Get data for charts and visualizations"""
    
    db = await get_database()
    user_id = current_user["id"]
    
    # Get documents from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    documents_cursor = db.documents.find({
        "user_id": user_id,
        "created_at": {"$gte": thirty_days_ago}
    })
    
    documents = []
    async for doc in documents_cursor:
        documents.append(doc)
    
    # Daily activity chart
    daily_activity = {}
    for doc in documents:
        date = doc.get("created_at", datetime.utcnow()).date()
        daily_activity[date] = daily_activity.get(date, 0) + 1
    
    # Fill missing days with 0
    for i in range(30):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        if date not in daily_activity:
            daily_activity[date] = 0
    
    daily_chart_data = [
        {"date": str(date), "count": count}
        for date, count in sorted(daily_activity.items())
    ]
    
    # File type distribution
    file_type_counts = {}
    for doc in documents:
        file_type = doc.get("file_type", "unknown")
        file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
    
    file_type_chart_data = [
        {"type": file_type, "count": count}
        for file_type, count in file_type_counts.items()
    ]
    
    # Processing time trends
    processing_times = [
        doc.get("processing_time", 0) for doc in documents
        if doc.get("processing_time") is not None
    ]
    
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    # Language distribution
    language_counts = {}
    for doc in documents:
        language = doc.get("language", "unknown")
        language_counts[language] = language_counts.get(language, 0) + 1
    
    language_chart_data = [
        {"language": lang, "count": count}
        for lang, count in language_counts.items()
    ]
    
    return {
        "daily_activity": daily_chart_data,
        "file_types": file_type_chart_data,
        "languages": language_chart_data,
        "average_processing_time": avg_processing_time,
        "total_processing_time": sum(processing_times)
    }
