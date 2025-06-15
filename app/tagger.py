# tagger.py

from keybert import KeyBERT
import spacy

# Load spaCy model and KeyBERT
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_keywords(text, top_n=5):
    """Extracts top keywords from the text using KeyBERT."""
    keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
    return [kw[0] for kw in keywords]

def extract_named_entities(text):
    """Extracts named entities using spaCy's NER pipeline."""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def categorize_text(text):
    """Basic rule-based categorization based on keyword matches."""
    categories = {
        "Finance": ["loan", "investment", "debt", "revenue", "bank"],
        "Legal": ["contract", "law", "compliance", "agreement", "court"],
        "Healthcare": ["patient", "treatment", "doctor", "hospital"],
        "Technology": ["AI", "machine learning", "software", "data", "algorithm"]
    }
    
    detected = []
    text_lower = text.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                detected.append(category)
                break
    return detected or ["Uncategorized"]

def tag_document(text):
    """Main function to return all tags for a document."""
    return {
        "keywords": extract_keywords(text),
        "entities": extract_named_entities(text),
        "categories": categorize_text(text)
    }
