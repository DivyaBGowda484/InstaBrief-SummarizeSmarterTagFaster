import nltk
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def summarize_extractive(text: str, num_sentences: int = 3) -> str:
    if not text.strip():
        return ""

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))

    word_frequencies = {}
    for word in words:
        if word.isalnum() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    max_freq = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)
