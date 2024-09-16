from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Topic Extraction using LDA
def extract_topics(transcription):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([transcription])
    
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X)
    
    topics = lda.components_
    topic_words = [[vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-5:-1]] for topic in topics]
    
    return topic_words

# Sentiment Analysis using VADER
def analyze_sentiment(transcription):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(transcription)
    
    return sentiment

# Generate Insights from transcription, topics, and sentiment
def generate_insights(transcription, topics, sentiment):
    insights = []
    if sentiment['compound'] > 0.5:
        insights.append("Overall sentiment is positive.")
    if 'price' in transcription:
        insights.append("Price discussion was prominent.")
    return insights
