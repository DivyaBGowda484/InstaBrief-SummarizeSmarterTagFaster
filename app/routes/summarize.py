from fastapi import APIRouter, HTTPException, Response, Depends
from app.models.schemas import SummaryRequest, SummaryResponse, TTSRequest, TTSResponse
from app.services.summarizer import SummarizerService
from app.services.tts import TTSService
from app.routes.auth import get_current_user
from bson import ObjectId
from datetime import datetime


router = APIRouter()
summarizer = SummarizerService()
tts_service = TTSService()


@router.post("/", response_model=SummaryResponse)
async def summarize_text(
    request: SummaryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate summary for text"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    try:
        # Initialize summarizer if needed
        await summarizer.initialize()
        
        # Generate summary
        result = await summarizer.generate_summary(
            request.text, 
            max_length=request.max_length,
            algorithm=request.algorithm
        )
        
        return SummaryResponse(
            id=str(ObjectId()),
            summary=result["summary"],
            original_length=result["original_length"],
            summary_length=result["summary_length"],
            compression_ratio=result["compression_ratio"],
            algorithm_used=result["algorithm_used"],
            processing_time=result["processing_time"],
            created_at=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(
    request: TTSRequest,
    current_user: dict = Depends(get_current_user)
):
    """Convert text to speech"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    try:
        # Generate audio
        audio_data = tts_service.synthesize(request.text, request.language)
        
        return TTSResponse(
            audio_url=f"/api/tts/audio/{str(ObjectId())}",
            duration=len(audio_data) / 16000,  # Estimate duration
            language=request.language,
            voice=request.voice or "default"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.get("/algorithms")
async def get_available_algorithms():
    """Get list of available summarization algorithms"""
    return {
        "algorithms": [
            {
                "name": "textrank",
                "display_name": "TextRank",
                "description": "Fast extractive summarization using graph-based ranking",
                "speed": "fast",
                "quality": "good"
            },
            {
                "name": "lsa",
                "display_name": "LSA (Latent Semantic Analysis)",
                "description": "Extractive summarization using singular value decomposition",
                "speed": "medium",
                "quality": "good"
            },
            {
                "name": "lexrank",
                "display_name": "LexRank",
                "description": "Graph-based summarization using centrality scoring",
                "speed": "medium",
                "quality": "very good"
            },
            {
                "name": "bert",
                "display_name": "BART (Advanced)",
                "description": "Abstractive summarization using transformer models",
                "speed": "slow",
                "quality": "excellent"
            }
        ]
    }


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese"}
        ]
    }
