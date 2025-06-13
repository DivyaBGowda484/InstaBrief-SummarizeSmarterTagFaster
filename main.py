from fastapi import FastAPI
from app.summarizer import summarize  
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to InstaBrief"}
@app.post("/summarize/")
def summarize_text(text: str):
    summary = summarize(text)
    if isinstance(summary, dict) and "text" in summary:
        summary = summary["text"]
    return {"summary": summary}
