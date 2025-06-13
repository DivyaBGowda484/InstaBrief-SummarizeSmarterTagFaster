import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
nlp = spacy.load("en_core_web_sm")
def extract_entities(text: str):
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents))
def extract_keywords(text: str, top_n: int = 5):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform([text])
    scores = zip(tfidf.get_feature_names_out(), tfidf_matrix.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_scores[:top_n]]
def get_tags(text: str):
    return {
        "entities": extract_entities(text),
        "keywords": extract_keywords(text)
    }
