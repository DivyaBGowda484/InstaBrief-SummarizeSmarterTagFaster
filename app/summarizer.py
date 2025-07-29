import re

def summarize_extractive(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    summary = ' '.join(sentences[:2])  # First 2 sentences
    return summary if summary else text

def summarize(text: str) -> str:
    return summarize_extractive(text)  # ✅ Return plain string
