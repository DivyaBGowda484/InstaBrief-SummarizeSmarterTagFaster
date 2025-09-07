from __future__ import annotations

from typing import Optional
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class SummarizerService:
    def __init__(self) -> None:
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def generate_summary(self, text: str, max_length: Optional[int] = 150) -> str:
        """Generate summary using extractive summarization"""
        if not text.strip():
            return ""
        
        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        
        # Use TextRank summarizer
        summarizer = TextRankSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        
        # Calculate number of sentences to extract
        sentences = parser.document.sentences
        if len(sentences) <= 2:
            return text
        
        # Estimate sentences needed based on max_length
        avg_sentence_length = len(text) / len(sentences)
        num_sentences = max(1, min(len(sentences) // 3, int(max_length / avg_sentence_length) if max_length else 3))
        
        # Generate summary
        summary_sentences = summarizer(parser.document, num_sentences)
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
        # If summary is too long, truncate it
        if max_length and len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        
        return summary.strip()

    def generate_summary_lsa(self, text: str, max_length: Optional[int] = 150) -> str:
        """Alternative summarization using LSA"""
        if not text.strip():
            return ""
        
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        
        sentences = parser.document.sentences
        if len(sentences) <= 2:
            return text
        
        num_sentences = max(1, min(len(sentences) // 3, int(max_length / (len(text) / len(sentences))) if max_length else 3))
        
        summary_sentences = summarizer(parser.document, num_sentences)
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
        if max_length and len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        
        return summary.strip()


