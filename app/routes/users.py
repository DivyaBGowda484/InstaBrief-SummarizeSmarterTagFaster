from fastapi import APIRouter, Depends
from app.utils.security import get_current_user
from app.services.storage import StorageService
from bson import ObjectId


router = APIRouter()
storage = StorageService()


@router.get('/me')
async def me(user=Depends(get_current_user)):
  return user


@router.get('/me/articles')
async def my_articles(user=Depends(get_current_user)):
  cursor = storage.db.articles.find({ 'owner_id': user['id'] })
  items = []
  async for doc in cursor:
    items.append({ 'id': str(doc['_id']), 'title': doc.get('title',''), 'content': doc.get('content',''), 'tags': doc.get('tags', []) })
  return items


