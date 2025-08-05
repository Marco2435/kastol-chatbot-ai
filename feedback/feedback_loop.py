
import csv
import os
from datetime import datetime

feedback_pad = "feedback/feedback.csv"

def registreer_feedback(vraag, antwoord, feedback_type):
    nieuw_item = [datetime.now().strftime("%Y-%m-%d %H:%M"), vraag, antwoord, feedback_type]
    bestaat = os.path.exists(feedback_pad)

    with open(feedback_pad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["tijd", "vraag", "antwoord", "feedbacktype"])
        writer.writerow(nieuw_item)


def registreer_verbeterde_feedback(vraag, fout_antwoord, correct_antwoord):
    pad = "feedback/trainingsdata.csv"
    bestaat = os.path.exists(pad)
    with open(pad, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not bestaat:
            writer.writerow(["tijd", "vraag", "fout_antwoord", "correct_antwoord", "feedbacktype"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), vraag, fout_antwoord, correct_antwoord, "correctie"])
