from __future__ import annotations

from typing import Any, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings
from app.services.nlp import NLPService


class StorageService:
    def __init__(self, mongo_uri: str | None = None) -> None:
        self.mongo = AsyncIOMotorClient(mongo_uri or settings.mongo_uri)
        self.db = self.mongo["instabrief"]
        self._nlp = NLPService()

    async def save_article(self, article: dict[str, Any]) -> str:
        # Add keywords and embedding to the article
        text_content = (article.get("title") or "") + "\n" + (article.get("content") or "")
        article["keywords"] = self._nlp.extract_keywords(text_content)
        article["embedding"] = self._nlp.compute_embedding(text_content)
        
        result = await self.db.articles.insert_one(article)
        return str(result.inserted_id)

    async def search_articles(self, query: str, size: int = 10):
        """Simple text search using MongoDB text search"""
        # Create a text index if it doesn't exist
        await self.db.articles.create_index([("title", "text"), ("content", "text")])
        
        # Perform text search
        cursor = self.db.articles.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(size)
        
        articles = await cursor.to_list(length=size)
        return [{"id": str(article["_id"]), **{k: v for k, v in article.items() if k != "_id"}} for article in articles]

    async def search_articles_semantic(self, query: str, size: int = 10):
        """Simple semantic search using keyword matching"""
        query_keywords = self._nlp.extract_keywords(query)
        
        # Search for articles with matching keywords
        pipeline = [
            {"$addFields": {
                "keyword_matches": {
                    "$size": {
                        "$setIntersection": ["$keywords", query_keywords]
                    }
                }
            }},
            {"$match": {"keyword_matches": {"$gt": 0}}},
            {"$sort": {"keyword_matches": -1}},
            {"$limit": size}
        ]
        
        cursor = self.db.articles.aggregate(pipeline)
        articles = await cursor.to_list(length=size)
        return [{"id": str(article["_id"]), **{k: v for k, v in article.items() if k not in ["_id", "keyword_matches"]}} for article in articles]

    async def get_article_by_id(self, article_id: str):
        """Get article by ID"""
        from bson import ObjectId
        article = await self.db.articles.find_one({"_id": ObjectId(article_id)})
        if article:
            return {"id": str(article["_id"]), **{k: v for k, v in article.items() if k != "_id"}}
        return None

    async def get_all_articles(self, skip: int = 0, limit: int = 10):
        """Get all articles with pagination"""
        cursor = self.db.articles.find().skip(skip).limit(limit).sort("_id", -1)
        articles = await cursor.to_list(length=limit)
        return [{"id": str(article["_id"]), **{k: v for k, v in article.items() if k != "_id"}} for article in articles]


