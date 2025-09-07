from __future__ import annotations

import time
import asyncio
from typing import Optional, Dict, Any
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import logging

logger = logging.getLogger(__name__)


class SummarizerService:
    def __init__(self) -> None:
        self.textrank_model = None
        self.lsa_model = None
        self.lexrank_model = None
        self.bert_model = None
        self.bert_tokenizer = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize all summarization models"""
        if self.initialized:
            return
            
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Initialize extractive models
            stemmer = Stemmer("english")
            stop_words = get_stop_words("english")
            
            self.textrank_model = TextRankSummarizer(stemmer)
            self.textrank_model.stop_words = stop_words
            
            self.lsa_model = LsaSummarizer(stemmer)
            self.lsa_model.stop_words = stop_words
            
            self.lexrank_model = LexRankSummarizer(stemmer)
            self.lexrank_model.stop_words = stop_words
            
            # Initialize abstractive model (BART)
            try:
                self.bert_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
                self.bert_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
                logger.info("BART model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load BART model: {e}")
                self.bert_model = None
                self.bert_tokenizer = None
            
            self.initialized = True
            logger.info("Summarizer service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize summarizer service: {e}")
            raise

    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = 150,
        algorithm: str = "textrank",
        min_length: Optional[int] = 50
    ) -> Dict[str, Any]:
        """Generate summary using specified algorithm"""
        if not self.initialized:
            await self.initialize()
            
        if not text.strip():
            return {
                "summary": "",
                "algorithm_used": algorithm,
                "processing_time": 0.0,
                "original_length": 0,
                "summary_length": 0,
                "compression_ratio": 0.0
            }
        
        start_time = time.time()
        
        try:
            if algorithm == "textrank":
                summary = await self._textrank_summary(text, max_length)
            elif algorithm == "lsa":
                summary = await self._lsa_summary(text, max_length)
            elif algorithm == "lexrank":
                summary = await self._lexrank_summary(text, max_length)
            elif algorithm == "bert":
                summary = await self._bert_summary(text, max_length, min_length)
            else:
                # Default to textrank
                summary = await self._textrank_summary(text, max_length)
                algorithm = "textrank"
            
            processing_time = time.time() - start_time
            
            return {
                "summary": summary,
                "algorithm_used": algorithm,
                "processing_time": processing_time,
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text) if len(text) > 0 else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                "summary": text[:max_length] + "..." if len(text) > max_length else text,
                "algorithm_used": "fallback",
                "processing_time": time.time() - start_time,
                "original_length": len(text),
                "summary_length": min(len(text), max_length),
                "compression_ratio": min(len(text), max_length) / len(text) if len(text) > 0 else 0.0
            }

    async def _textrank_summary(self, text: str, max_length: int) -> str:
        """Generate summary using TextRank algorithm"""
        def _summarize():
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            sentences = parser.document.sentences
            
            if len(sentences) <= 2:
                return text
            
            # Calculate number of sentences to extract
            avg_sentence_length = len(text) / len(sentences)
            num_sentences = max(1, min(len(sentences) // 3, int(max_length / avg_sentence_length) if max_length else 3))
            
            summary_sentences = self.textrank_model(parser.document, num_sentences)
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            
            if max_length and len(summary) > max_length:
                summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
            
            return summary.strip()
        
        return await asyncio.get_event_loop().run_in_executor(None, _summarize)

    async def _lsa_summary(self, text: str, max_length: int) -> str:
        """Generate summary using LSA algorithm"""
        def _summarize():
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            sentences = parser.document.sentences
            
            if len(sentences) <= 2:
                return text
            
            avg_sentence_length = len(text) / len(sentences)
            num_sentences = max(1, min(len(sentences) // 3, int(max_length / avg_sentence_length) if max_length else 3))
            
            summary_sentences = self.lsa_model(parser.document, num_sentences)
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            
            if max_length and len(summary) > max_length:
                summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
            
            return summary.strip()
        
        return await asyncio.get_event_loop().run_in_executor(None, _summarize)

    async def _lexrank_summary(self, text: str, max_length: int) -> str:
        """Generate summary using LexRank algorithm"""
        def _summarize():
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            sentences = parser.document.sentences
            
            if len(sentences) <= 2:
                return text
            
            avg_sentence_length = len(text) / len(sentences)
            num_sentences = max(1, min(len(sentences) // 3, int(max_length / avg_sentence_length) if max_length else 3))
            
            summary_sentences = self.lexrank_model(parser.document, num_sentences)
            summary = " ".join([str(sentence) for sentence in summary_sentences])
            
            if max_length and len(summary) > max_length:
                summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
            
            return summary.strip()
        
        return await asyncio.get_event_loop().run_in_executor(None, _summarize)

    async def _bert_summary(self, text: str, max_length: int, min_length: int = 50) -> str:
        """Generate summary using BART model"""
        if not self.bert_model or not self.bert_tokenizer:
            # Fallback to textrank if BART is not available
            return await self._textrank_summary(text, max_length)
        
        def _summarize():
            # Truncate input if too long (BART has input limits)
            max_input_length = 1024
            if len(text) > max_input_length:
                text = text[:max_input_length]
            
            inputs = self.bert_tokenizer(
                text, 
                max_length=max_input_length, 
                truncation=True, 
                return_tensors="pt"
            )
            
            with torch.no_grad():
                summary_ids = self.bert_model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            
            summary = self.bert_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()
        
        return await asyncio.get_event_loop().run_in_executor(None, _summarize)

    async def generate_multi_algorithm_summary(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate summaries using multiple algorithms and return the best one"""
        if not self.initialized:
            await self.initialize()
        
        algorithms = ["textrank", "lsa", "lexrank"]
        if self.bert_model:
            algorithms.append("bert")
        
        results = {}
        for algorithm in algorithms:
            try:
                result = await self.generate_summary(text, max_length, algorithm)
                results[algorithm] = result
            except Exception as e:
                logger.error(f"Error with {algorithm}: {e}")
                continue
        
        # Select best summary based on compression ratio and processing time
        best_algorithm = None
        best_score = 0
        
        for algorithm, result in results.items():
            # Score based on compression ratio and processing time
            compression_score = result["compression_ratio"] if result["compression_ratio"] > 0 else 0
            time_score = 1.0 / (result["processing_time"] + 0.1)  # Avoid division by zero
            combined_score = compression_score * 0.7 + time_score * 0.3
            
            if combined_score > best_score:
                best_score = combined_score
                best_algorithm = algorithm
        
        if best_algorithm and best_algorithm in results:
            best_result = results[best_algorithm]
            best_result["all_algorithms"] = results
            return best_result
        else:
            # Fallback to simple truncation
            return {
                "summary": text[:max_length] + "..." if len(text) > max_length else text,
                "algorithm_used": "fallback",
                "processing_time": 0.0,
                "original_length": len(text),
                "summary_length": min(len(text), max_length),
                "compression_ratio": min(len(text), max_length) / len(text) if len(text) > 0 else 0.0
            }


