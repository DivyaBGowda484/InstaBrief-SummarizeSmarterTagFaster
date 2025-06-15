# app/summarizer.py

from typing import Dict

# Dummy extractive summarization function
def summarize_extractive(text: str) -> str:
    """
    Returns the first 2 sentences as a basic extractive summary.
    Replace this with actual summarization logic using NLP models later.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    summary = ' '.join(sentences[:2])  # Take first 2 sentences
    return summary if summary else text

# Wrapper for consistency with your FastAPI route
def summarize(text: str) -> Dict[str, str]:
    summary = summarize_extractive(text)
    return {"text": summary}
