# This module generates a summary of the cleaned text using a pre-trained transformer model.
# It uses the Hugging Face Transformers library to load a summarization pipeline.
# The generated summary is returned as a string.
# The summarization pipeline uses a pre-trained model to generate a summary of the input text.

from transformers import pipeline

summarizer = pipeline("summarization")

def generate_summary(text):
    # Limit input to first 1024 tokens due to model constraints
    return summarizer(text[:1024])[0]['summary_text']

