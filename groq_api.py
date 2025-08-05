
import os
import requests

def vraag_aan_groq(prompt, context, taal="NL"):
    """
    Stuurt een prompt naar Groq API (model via .env: MODEL=...) en geeft het antwoord terug.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("MODEL", "llama3-70b-4096")

    if not api_key:
        return "❌ Fout: Geen GROQ_API_KEY gevonden in omgeving."

    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Beantwoord vragen professioneel en beknopt."},
            {"role": "user", "content": f"Context: {context}\n\nVraag: {prompt}"}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Fout bij Groq API: {e}"

def get_embedding(tekst):
    """
    Momenteel nog niet ondersteund via Groq. Geeft dummy embedding terug.
    """
    return [0.0] * 1536
