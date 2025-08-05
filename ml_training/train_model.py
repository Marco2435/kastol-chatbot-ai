
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def train_model():
    df = pd.read_csv("ml_training/train.csv")
    X, y = df["question"], df["answer"]
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    pipe.fit(X, y)
    joblib.dump(pipe, "ml_training/model.pkl")
    return pipe
