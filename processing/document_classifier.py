
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import csv
from datetime import datetime

class DocumentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self.trained = False

    def train(self, voorbeelden):
        texts = [v["inhoud"] for v in voorbeelden]
        labels = [v["label"] for v in voorbeelden]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.trained = True

    def predict(self, tekst):
        if not self.trained:
            return "onbekend"
        X_new = self.vectorizer.transform([tekst])
        return self.model.predict(X_new)[0]

def log_classificatie(bestandsnaam, label):
    pad = "logs/classified_docs.csv"
    bestaat = os.path.exists(pad)
    with open(pad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["tijd", "bestand", "label"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), bestandsnaam, label])
