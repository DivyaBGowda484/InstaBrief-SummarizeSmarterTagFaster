from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch
from config.settings import settings
import asyncio


class Database:
    client: AsyncIOMotorClient = None
    elasticsearch: AsyncElasticsearch = None


db = Database()


async def get_database():
    return db.client[settings.database_name]


async def get_elasticsearch():
    return db.elasticsearch


async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.mongo_uri)
    try:
        # Test the connection
        await db.client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


async def connect_to_elasticsearch():
    """Create Elasticsearch connection"""
    db.elasticsearch = AsyncElasticsearch([settings.elasticsearch_url])
    try:
        # Test the connection
        await db.elasticsearch.ping()
        print("Connected to Elasticsearch!")
        
        # Create index if it doesn't exist
        if not await db.elasticsearch.indices.exists(index=settings.elasticsearch_index):
            await create_elasticsearch_index()
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")


async def create_elasticsearch_index():
    """Create Elasticsearch index with proper mapping"""
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"},
                "summary": {"type": "text", "analyzer": "standard"},
                "tags": {"type": "keyword"},
                "user_id": {"type": "keyword"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
                "file_type": {"type": "keyword"},
                "file_size": {"type": "long"},
                "language": {"type": "keyword"},
                "sentiment": {"type": "keyword"},
                "entities": {"type": "keyword"},
                "topics": {"type": "keyword"}
            }
        }
    }
    
    await db.elasticsearch.indices.create(
        index=settings.elasticsearch_index,
        body=mapping
    )
    print(f"Created Elasticsearch index: {settings.elasticsearch_index}")


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()


async def close_elasticsearch_connection():
    """Close Elasticsearch connection"""
    if db.elasticsearch:
        await db.elasticsearch.close()