from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def choose_model(text):
    legal_keywords = ["court", "legal", "law", "judgment", "contract", "statute", "case"]
    tfidf = TfidfVectorizer(vocabulary=legal_keywords)
    tfidf_matrix = tfidf.fit_transform([text.lower()])
    score = np.sum(tfidf_matrix.toarray())
    
    if score > 0.1:
        return "legalbert"
    elif len(text.split()) > 50:
        return "pegasus"
    return "bert"