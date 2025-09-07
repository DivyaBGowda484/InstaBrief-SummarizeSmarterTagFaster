import spacy
import nltk
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class NLPService:
    def __init__(self):
        self.nlp = None
        self.sentence_model = None
        self.tfidf_vectorizer = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    async def initialize(self):
        """Initialize NLP models asynchronously"""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            
            # Load sentence transformer model
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            
            logger.info("NLP models initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NLP models: {e}")
            raise

    async def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities from text"""
        if not self.nlp:
            await self.initialize()
            
        def _extract():
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            return entities
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _extract
        )

    async def extract_keywords(self, text: str, max_keywords: int = 10) -> List[Dict[str, float]]:
        """Extract keywords using TF-IDF"""
        if not self.tfidf_vectorizer:
            await self.initialize()
            
        def _extract():
            # Clean and tokenize text
            sentences = nltk.sent_tokenize(text)
            if not sentences:
                return []
            
            # Fit TF-IDF
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get mean TF-IDF scores
            mean_scores = tfidf_matrix.mean(axis=0).A1
            word_scores = list(zip(feature_names, mean_scores))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [{"word": word, "score": float(score)} 
                   for word, score in word_scores[:max_keywords]]
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _extract
        )

    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text"""
        if not self.nlp:
            await self.initialize()
            
        def _analyze():
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            return {
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "compound": scores["compound"]
            }
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _analyze
        )

    async def detect_language(self, text: str) -> str:
        """Detect language of text"""
        if not self.nlp:
            await self.initialize()
            
        def _detect():
            doc = self.nlp(text[:1000])  # Use first 1000 chars for speed
            return doc.lang_
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _detect
        )

    async def extract_topics(self, text: str, num_topics: int = 5) -> List[Dict[str, float]]:
        """Extract topics using LDA (simplified version)"""
        if not self.tfidf_vectorizer:
            await self.initialize()
            
        def _extract():
            from sklearn.decomposition import LatentDirichletAllocation
            
            # Clean text
            sentences = nltk.sent_tokenize(text)
            if len(sentences) < 2:
                return []
            
            # Vectorize
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)
            
            # LDA
            lda = LatentDirichletAllocation(
                n_components=min(num_topics, len(sentences)),
                random_state=42
            )
            lda.fit(tfidf_matrix)
            
            # Get topic words
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-5:][::-1]
                top_words = [(feature_names[i], topic[i]) for i in top_words_idx]
                topics.append({
                    "topic_id": topic_idx,
                    "words": [{"word": word, "weight": float(weight)} for word, weight in top_words]
                })
            
            return topics
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _extract
        )

    async def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        if not self.sentence_model:
            await self.initialize()
            
        def _calculate():
            embeddings = self.sentence_model.encode([text1, text2])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _calculate
        )

    async def extract_phrases(self, text: str, min_length: int = 2, max_length: int = 4) -> List[str]:
        """Extract meaningful phrases from text"""
        if not self.nlp:
            await self.initialize()
            
        def _extract():
            doc = self.nlp(text)
            phrases = []
            
            # Extract noun phrases
            for chunk in doc.noun_chunks:
                if min_length <= len(chunk.text.split()) <= max_length:
                    phrases.append(chunk.text.strip())
            
            # Extract named entities as phrases
            for ent in doc.ents:
                if min_length <= len(ent.text.split()) <= max_length:
                    phrases.append(ent.text.strip())
            
            return list(set(phrases))  # Remove duplicates
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _extract
        )

    async def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        def _clean():
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s.,!?;:-]', '', text)
            # Normalize unicode
            text = text.encode('utf-8').decode('utf-8')
            return text.strip()
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _clean
        )

    async def get_text_statistics(self, text: str) -> Dict[str, any]:
        """Get comprehensive text statistics"""
        if not self.nlp:
            await self.initialize()
            
        def _analyze():
            doc = self.nlp(text)
            
            # Basic stats
            word_count = len([token for token in doc if not token.is_space])
            sentence_count = len(list(doc.sents))
            char_count = len(text)
            
            # Readability metrics
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            avg_word_length = sum(len(token.text) for token in doc if not token.is_space) / word_count if word_count > 0 else 0
            
            # POS tags
            pos_counts = {}
            for token in doc:
                if not token.is_space:
                    pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
            
            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "character_count": char_count,
                "avg_sentence_length": avg_sentence_length,
                "avg_word_length": avg_word_length,
                "pos_counts": pos_counts,
                "reading_time_minutes": word_count / 200  # Assuming 200 WPM
            }
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, _analyze
        )

    def __del__(self):
        """Cleanup executor"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)