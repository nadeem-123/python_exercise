import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

data = {
    'Headline': [
        "Market hits all-time high as tech stocks rally",
        "Economic downturn expected in the next quarter",
        "Company announces breakthrough in AI technology",
        "Investors worried as inflation rises",
        "Stock prices soar after earnings report"
    ],
    'Sentiment': [1, 0, 1, 0, 1]  # 1 = Positive, 0 = Negative
}

df = pd.DataFrame(data)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(filtered_tokens)

df['Cleaned_Headline'] = df['Headline'].apply(preprocess_text)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Cleaned_Headline']).toarray()
y = df['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

new_headlines = [
    "Tech companies see unprecedented growth",
    "Global recession fears loom large"
]

new_headlines_cleaned = [preprocess_text(headline) for headline in new_headlines]
new_features = vectorizer.transform(new_headlines_cleaned).toarray()
predictions = model.predict(new_features)

for headline, sentiment in zip(new_headlines, predictions):
    print(f"Headline: {headline} | Sentiment: {'Positive' if sentiment == 1 else 'Negative'}")

