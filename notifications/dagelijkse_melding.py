
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
import csv

def verzend_dagelijkse_samenvatting():
    feedback_path = "feedback/feedback.csv"
    laatste_feedback = ""
    if os.path.exists(feedback_path):
        with open(feedback_path, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                laatste = rows[-1]
                laatste_feedback = f"Laatste feedback:\nVraag: {laatste[0]}\nAntwoord: {laatste[1]}\nType: {laatste[2]}\n"

    nu = datetime.now().strftime("%Y-%m-%d %H:%M")
    inhoud = (
        "Dagelijkse samenvatting Kastol AI Chatbot\n\n"
        f"Tijdstip: {nu}\n\n"
        f"{laatste_feedback if laatste_feedback else 'Geen feedback vandaag geregistreerd.'}\n\n"
        "Met vriendelijke groet,\nKastol AI Chatbot"
    )

    msg = EmailMessage()
    msg.set_content(inhoud)
    msg["Subject"] = "Dagelijkse samenvatting Kastol AI"
    msg["From"] = os.getenv("EMAIL_AFZENDER")
    msg["To"] = os.getenv("EMAIL_ADMIN")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_AFZENDER"), os.getenv("EMAIL_WACHTWOORD"))
            server.send_message(msg)
    except Exception as e:
        print("Fout bij verzenden e-mail:", e)

if __name__ == "__main__":
    verzend_dagelijkse_samenvatting()
