from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.summarizer import summarize
from app.tagger import tag_document
from app.speech import text_to_speech

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input
class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to InstaBrief – Summarize Smarter, Tag Faster!"}

@app.post("/summarize/")
def summarize_text(input: TextInput):
    try:
        summary = summarize(input.text)  # returns string now
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tag/")
def tag_text(input: TextInput):
    try:
        tags = tag_document(input.text)
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak/")
def speak_text(input: TextInput):
    try:
        audio_path = text_to_speech(input.text)
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Add your PDF/DOCX extraction logic here
        return {"filename": file.filename, "size_bytes": len(contents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
