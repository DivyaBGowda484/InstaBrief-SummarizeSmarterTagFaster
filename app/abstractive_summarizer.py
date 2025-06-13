from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_abstractive(text: str, max_length=150, min_length=40) -> str:
    summary = summarizer_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
