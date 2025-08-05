
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import csv
from datetime import datetime

class AnomalyDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = IsolationForest(contamination=0.05)
        self.vragen = []

    def fit(self, vragen):
        self.vragen = vragen
        X = self.vectorizer.fit_transform(vragen)
        self.model.fit(X)

    def is_anomalie(self, nieuwe_vraag):
        if not self.vragen:
            return False, 0.0
        X_new = self.vectorizer.transform([nieuwe_vraag])
        score = self.model.decision_function(X_new)[0]
        prediction = self.model.predict(X_new)[0]
        return prediction == -1, score

def log_anomalie(vraag, score):
    pad = "logs/anomalies.csv"
    bestaat = os.path.exists(pad)
    with open(pad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["tijd", "vraag", "score"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), vraag, round(score, 4)])
