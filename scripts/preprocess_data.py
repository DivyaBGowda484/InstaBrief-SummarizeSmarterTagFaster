# This module preprocesses the extracted text by cleaning it.
# It removes extra spaces, punctuation, and stop words.
# The cleaned text is returned as a string.

import re
from nltk.corpus import stopwords 
import nltk

# Ensure stopwords are downloaded
nltk.download('stopwords', quiet=True)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    return " ".join([word for word in text.split() if word not in stop_words])
