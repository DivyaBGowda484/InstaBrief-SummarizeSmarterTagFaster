from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]

    # MongoDB configuration
    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "instabrief"

    # Elasticsearch configuration
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_index: str = "instabrief_documents"

    # File upload settings
    max_file_size: int = 25 * 1024 * 1024  # 25MB
    allowed_file_types: List[str] = [".pdf", ".docx", ".txt", ".pptx"]
    upload_directory: str = "uploads"

    # AI Model settings
    default_summary_length: int = 150
    max_summary_length: int = 500
    enable_tts: bool = True
    enable_advanced_nlp: bool = True

    # API settings
    api_v1_prefix: str = "/api/v1"
    project_name: str = "InstaBrief"
    version: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()


