import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main  
from .extractive_summarizer import summarize_extractive
from .abstractive_summarizer import summarize_abstractive

def summarize(text: str, method: str = "extractive") -> str:
    if method == "abstractive":
        return summarize_abstractive(text)
    return summarize_extractive(text)
