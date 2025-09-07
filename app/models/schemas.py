from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"


class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    PPTX = "pptx"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    created_at: datetime
    is_active: bool = True


class UserInDB(UserPublic):
    hashed_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic


class DocumentCreate(BaseModel):
    title: str
    content: str
    file_type: Optional[FileType] = None
    tags: List[str] = Field(default_factory=list)
    language: Optional[str] = "en"


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class DocumentPublic(BaseModel):
    id: str
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    file_type: Optional[FileType] = None
    file_size: Optional[int] = None
    language: Optional[str] = None
    sentiment: Optional[str] = None
    entities: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: datetime
    updated_at: datetime
    user_id: str


class DocumentInDB(DocumentPublic):
    pass


class SummaryRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    algorithm: Optional[str] = "textrank"  # textrank, lsa, bert
    language: Optional[str] = "en"


class SummaryResponse(BaseModel):
    id: str
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float
    algorithm_used: str
    processing_time: float
    created_at: datetime


class TagRequest(BaseModel):
    text: str
    max_tags: Optional[int] = 10
    include_entities: bool = True
    include_topics: bool = True


class TagResponse(BaseModel):
    tags: List[str]
    entities: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)


class SearchRequest(BaseModel):
    query: str
    semantic: bool = False
    filters: Optional[Dict[str, Any]] = None
    page: int = 0
    limit: int = 20


class SearchResponse(BaseModel):
    results: List[DocumentPublic]
    total: int
    page: int
    limit: int
    query: str
    processing_time: float


class FeedbackCreate(BaseModel):
    document_id: str
    helpful: bool
    rating: Optional[int] = Field(None, ge=1, le=5)
    comments: Optional[str] = None
    summary_quality: Optional[int] = Field(None, ge=1, le=5)
    tag_accuracy: Optional[int] = Field(None, ge=1, le=5)


class FeedbackPublic(BaseModel):
    id: str
    document_id: str
    helpful: bool
    rating: Optional[int] = None
    comments: Optional[str] = None
    summary_quality: Optional[int] = None
    tag_accuracy: Optional[int] = None
    created_at: datetime
    user_id: str


class AnalyticsResponse(BaseModel):
    total_documents: int
    total_summaries: int
    total_tags: int
    time_saved_hours: float
    efficiency_gain_percent: float
    documents_by_type: Dict[str, int]
    recent_activity: List[DocumentPublic]
    top_tags: List[Dict[str, Any]]
    processing_stats: Dict[str, Any]


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice: Optional[str] = None


class TTSResponse(BaseModel):
    audio_url: str
    duration: float
    language: str
    voice: str


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    file_size: int
    upload_url: Optional[str] = None
    processing_status: ProcessingStatus


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


