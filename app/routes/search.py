from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime

from app.models.schemas import SearchRequest, SearchResponse, DocumentPublic
from app.routes.auth import get_current_user
from config.db import get_elasticsearch

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search_documents(
    q: str = Query(..., description="Search query"),
    semantic: bool = Query(False, description="Use semantic search"),
    type: Optional[str] = Query(None, description="Filter by file type"),
    date_range: Optional[str] = Query(None, description="Filter by date range"),
    sort: str = Query("relevance", description="Sort order"),
    page: int = Query(0, ge=0, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    current_user: dict = Depends(get_current_user)
):
    """Search documents using Elasticsearch"""
    
    try:
        es = await get_elasticsearch()
        
        # Build query
        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "user_id": current_user["id"]
                            }
                        }
                    ]
                }
            },
            "from": page * limit,
            "size": limit
        }
        
        # Add text search
        if q:
            if semantic:
                # Semantic search using vector similarity
                query_body["query"]["bool"]["must"].append({
                    "multi_match": {
                        "query": q,
                        "fields": ["title^2", "content", "summary^1.5", "tags"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                })
            else:
                # Regular text search
                query_body["query"]["bool"]["must"].append({
                    "multi_match": {
                        "query": q,
                        "fields": ["title^2", "content", "summary^1.5", "tags"],
                        "type": "best_fields"
                    }
                })
        
        # Add filters
        if type and type != "all":
            query_body["query"]["bool"]["filter"] = query_body["query"]["bool"].get("filter", [])
            query_body["query"]["bool"]["filter"].append({
                "term": {"file_type": type}
            })
        
        if date_range and date_range != "all":
            now = datetime.utcnow()
            if date_range == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_range == "week":
                start_date = now.replace(day=now.day-7)
            elif date_range == "month":
                start_date = now.replace(month=now.month-1)
            elif date_range == "year":
                start_date = now.replace(year=now.year-1)
            else:
                start_date = None
            
            if start_date:
                query_body["query"]["bool"]["filter"] = query_body["query"]["bool"].get("filter", [])
                query_body["query"]["bool"]["filter"].append({
                    "range": {
                        "created_at": {
                            "gte": start_date.isoformat()
                        }
                    }
                })
        
        # Add sorting
        if sort == "newest":
            query_body["sort"] = [{"created_at": {"order": "desc"}}]
        elif sort == "oldest":
            query_body["sort"] = [{"created_at": {"order": "asc"}}]
        elif sort == "name":
            query_body["sort"] = [{"title.keyword": {"order": "asc"}}]
        elif sort == "size":
            query_body["sort"] = [{"file_size": {"order": "desc"}}]
        else:  # relevance
            query_body["sort"] = ["_score"]
        
        # Execute search
        start_time = datetime.utcnow()
        response = await es.search(
            index="instabrief_documents",
            body=query_body
        )
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Process results
        results = []
        for hit in response["hits"]["hits"]:
            doc = hit["_source"]
            doc["id"] = hit["_id"]
            results.append(DocumentPublic(**doc))
        
        return SearchResponse(
            results=results,
            total=response["hits"]["total"]["value"],
            page=page,
            limit=limit,
            query=q,
            processing_time=processing_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/suggest")
async def search_suggestions(
    q: str = Query(..., description="Search query"),
    current_user: dict = Depends(get_current_user)
):
    """Get search suggestions"""
    
    try:
        es = await get_elasticsearch()
        
        # Get suggestions from tags and titles
        query_body = {
            "suggest": {
                "tag_suggest": {
                    "prefix": q,
                    "completion": {
                        "field": "tags_suggest",
                        "size": 5
                    }
                },
                "title_suggest": {
                    "prefix": q,
                    "completion": {
                        "field": "title_suggest",
                        "size": 5
                    }
                }
            }
        }
        
        response = await es.search(
            index="instabrief_documents",
            body=query_body
        )
        
        suggestions = []
        
        # Process tag suggestions
        if "tag_suggest" in response["suggest"]:
            for option in response["suggest"]["tag_suggest"][0]["options"]:
                suggestions.append({
                    "text": option["text"],
                    "type": "tag",
                    "score": option["_score"]
                })
        
        # Process title suggestions
        if "title_suggest" in response["suggest"]:
            for option in response["suggest"]["title_suggest"][0]["options"]:
                suggestions.append({
                    "text": option["text"],
                    "type": "title",
                    "score": option["_score"]
                })
        
        # Sort by score and return top 10
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions[:10]
    
    except Exception as e:
        return []
