from __future__ import annotations

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import hashlib


class NLPService:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def extract_entities(self, text: str):
        """Simple entity extraction using NLTK"""
        tokens = word_tokenize(text)
        # Simple approach: return capitalized words as potential entities
        entities = []
        for token in tokens:
            if token[0].isupper() and len(token) > 2:
                entities.append((token, 'PERSON'))  # Simplified entity type
        return entities

    def compute_embedding(self, text: str):
        """Simple text embedding using hash-based approach"""
        # Create a simple hash-based embedding (384 dimensions to match original)
        hash_obj = hashlib.sha256(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert hex to list of integers and normalize
        embedding = []
        for i in range(0, len(hash_hex), 2):
            if len(embedding) >= 384:
                break
            embedding.append(int(hash_hex[i:i+2], 16) / 255.0)
        
        # Pad or truncate to exactly 384 dimensions
        while len(embedding) < 384:
            embedding.append(0.0)
        
        return embedding[:384]

    def extract_keywords(self, text: str, num_keywords: int = 10):
        """Extract keywords using NLTK"""
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        
        # Filter out stopwords and short words
        keywords = [word for word in tokens if word.isalnum() and word not in stop_words and len(word) > 2]
        
        # Count frequency
        from collections import Counter
        keyword_freq = Counter(keywords)
        
        return [word for word, freq in keyword_freq.most_common(num_keywords)]


