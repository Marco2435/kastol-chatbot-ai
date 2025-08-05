
import pandas as pd
from sklearn.metrics import classification_report
import joblib

def evaluate_model():
    df = pd.read_csv("ml_training/test.csv")
    model = joblib.load("ml_training/model.pkl")
    y_true = df["answer"]
    y_pred = model.predict(df["question"])
    report = classification_report(y_true, y_pred, zero_division=0)
    with open("ml_training/evaluation.txt", "w") as f:
        f.write(report)
    print(report)
