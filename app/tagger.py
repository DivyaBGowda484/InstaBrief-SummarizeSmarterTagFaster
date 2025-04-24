# Importing necessary libraries
from keybert import KeyBERT  # For extracting keywords from text
import spacy  # For performing Named Entity Recognition (NER)
from transformers import pipeline  # For zero-shot classification using pre-trained models

# Keyword Extraction
# Initialize the KeyBERT model for extracting keywords
kw_model = KeyBERT()

def extract_keywords(text, top_n=5):
    """
    Extracts the most relevant keywords from the given text using the KeyBERT model.

    Parameters:
        text (str): The input text from which to extract keywords.
        top_n (int): The number of top keywords to extract. Default is 5.

    Returns:
        list: A list of keywords as strings, ranked by relevance.
    """
    # Use KeyBERT to extract keywords and return only the keyword strings
    return [kw[0] for kw in kw_model.extract_keywords(text, top_n=top_n)]

# Named Entity Recognition
# Load the spaCy language model for identifying named entities in text
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extracts named entities from the given text using spaCy's NER model.

    Parameters:
        text (str): The input text from which to extract named entities.

    Returns:
        list: A list of tuples where each tuple contains:
              - The entity text (str)
              - The entity label (str), e.g., PERSON, ORG, GPE, etc.
    """
    # Process the text using spaCy's NLP pipeline
    doc = nlp(text)
    # Extract and return entities and their labels
    return [(ent.text, ent.label_) for ent in doc.ents]

# Zero-Shot Classification
# Initialize the Hugging Face pipeline for zero-shot classification
classifier = pipeline("zero-shot-classification")

def classify_document(text, labels):
    """
    Classifies the given text into one of the provided labels using zero-shot classification.

    Parameters:
        text (str): The input text to classify.
        labels (list): A list of candidate labels for classification.

    Returns:
        str: The label with the highest confidence score.
    """
    # Perform zero-shot classification and return the label with the highest confidence
    result = classifier(text, candidate_labels=labels)
    return result['labels'][0]