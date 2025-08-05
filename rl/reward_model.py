
import os
import csv
from datetime import datetime

def log_reward(vraag, antwoord, correctie=None, score=0):
    pad = "logs/reward_training_data.csv"
    bestaat = os.path.exists(pad)
    with open(pad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["tijd", "vraag", "antwoord", "correctie", "score"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), vraag, antwoord, correctie or "", score])
