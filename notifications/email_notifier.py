
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

def send_email_notification(vraag, antwoord):
    try:
        ontvanger = os.getenv("EMAIL_RECEIVER")
        if not ontvanger:
            return

        msg = EmailMessage()
        msg["Subject"] = "❗ Negatieve feedback op Kastol Chatbot"
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = ontvanger
        msg.set_content(f"""Er is negatieve feedback gegeven.

Vraag:
{vraag}

Antwoord:
{antwoord}

Tijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
        with smtplib.SMTP_SSL(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
    except Exception as e:
        print(f"Email fout: {e}")


def stuur_email_naar_gebruiker(ontvanger, sessie_inhoud):
    msg = EmailMessage()
    msg.set_content(sessie_inhoud)
    msg["Subject"] = "Jouw chat met Kastol AI Chatbot"
    msg["From"] = os.getenv("EMAIL_AFZENDER")
    msg["To"] = ontvanger

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_AFZENDER"), os.getenv("EMAIL_WACHTWOORD"))
            server.send_message(msg)
        return True
    except Exception as e:
        print("Fout bij verzenden sessie-email:", e)
        return False
