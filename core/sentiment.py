# core/sentiment.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

def classify_text(text: str) -> str:
    scores = analyzer.polarity_scores(str(text))
    compound = scores["compound"]
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"
