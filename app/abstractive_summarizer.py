from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
import torch

# Efficient loading
device = 0 if torch.cuda.is_available() else -1
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def chunk_text(text, chunk_size=1024):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def summarize_abstractive(text: str, max_length=150, min_length=40) -> str:
    try:
        summaries = []
        for chunk in chunk_text(text):
            result = summarizer_pipeline(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(result[0]['summary_text'])
        return " ".join(summaries)
    except Exception as e:
        return f"Summarization failed: {e}"
