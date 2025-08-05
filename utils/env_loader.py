
import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    # eventueel kun je hier controleren of belangrijke vars aanwezig zijn
    required = ["GROQ_API_KEY", "MODEL", "EMAIL_USER", "EMAIL_PASS", "EMAIL_RECEIVER"]
    for var in required:
        if not os.getenv(var):
            print(f"⚠️  Waarschuwing: omgevingsvariabele '{var}' ontbreekt.")
