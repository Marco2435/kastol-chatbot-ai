
import csv
from datetime import datetime

def sla_feedback_op(vraag, antwoord, feedback, bestand='feedback_logs.csv'):
    with open(bestand, mode='a', newline='', encoding='utf-8') as f:
        schrijver = csv.writer(f)
        schrijver.writerow([datetime.now(), vraag, antwoord, feedback])

def registreer_feedback(vraag, antwoord, tevreden=True):
    feedback = "Tevreden" if tevreden else "Ontevreden"
    sla_feedback_op(vraag, antwoord, feedback)

def registreer_verbeterde_feedback(vraag, antwoord, verbeterd_antwoord):
    feedback = f"Verbeterd: {verbeterd_antwoord}"
    sla_feedback_op(vraag, antwoord, feedback)
