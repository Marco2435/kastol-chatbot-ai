
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def stuur_email(onderwerp, bericht, ontvanger=EMAIL_USER):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ontvanger
    msg["Subject"] = onderwerp

    msg.attach(MIMEText(bericht, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ E-mail verzonden naar {ontvanger}")
    except Exception as e:
        print(f"❌ Fout bij verzenden e-mail: {e}")

def stuur_email_naar_gebruiker(ontvanger_email, onderwerp, bericht):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ontvanger_email
    msg["Subject"] = onderwerp

    msg.attach(MIMEText(bericht, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Gebruikersmail verzonden naar {ontvanger_email}")
    except Exception as e:
        print(f"❌ Fout bij verzenden gebruikersmail: {e}")
