
import streamlit as st
import os
import pandas as pd
import pytesseract
from PIL import Image
import PyPDF2
import docx
from groq import Groq

# Initialiseer Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def laad_data_map(pad="data"):
    context = []
    for bestandsnaam in os.listdir(pad):
        volledig_pad = os.path.join(pad, bestandsnaam)
        if bestandsnaam.endswith(".pdf"):
            context.append(lees_pdf(volledig_pad))
        elif bestandsnaam.endswith(".txt"):
            context.append(lees_txt(volledig_pad))
        elif bestandsnaam.endswith(".docx"):
            context.append(lees_docx(volledig_pad))
        elif bestandsnaam.endswith(".xlsx"):
            context.append(verwerk_excel(volledig_pad))
        elif bestandsnaam.lower().endswith(('.png', '.jpg', '.jpeg')):
            context.append(ocr_afbeelding(volledig_pad))
    return "\n".join(context)

def lees_pdf(pad):
    try:
        with open(pad, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            tekst = ""
            for pagina in reader.pages:
                tekst += pagina.extract_text() or ""
            return tekst
    except:
        return ""

def lees_txt(pad):
    with open(pad, "r", encoding="utf-8") as f:
        return f.read()

def lees_docx(pad):
    doc = docx.Document(pad)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

def ocr_afbeelding(pad):
    try:
        img = Image.open(pad)
        return pytesseract.image_to_string(img, lang='nld')
    except:
        return ""

def verwerk_excel(pad):
    try:
        df = pd.read_excel(pad)
        regels = []
        for _, rij in df.iterrows():
            naam = str(rij.get("Naam", ""))
            ref = str(rij.get("Referentie", ""))
            prijs = rij.get("Bruto Prijs", "")
            regels.append(f"{naam}: artikelnummer {ref}, prijs €{prijs}")
        return "\n".join(regels)
    except:
        return ""

def run_chat():
    st.title("Kastol AI Chatbot 🤖")
    vraag = st.text_input("Wat wil je weten over een product of document?", "")
    if vraag:
        st.info("Even geduld, ik zoek het voor je uit...")
        context = laad_data_map("data")
        antwoord = vraag_aan_groq(vraag, context)
        st.markdown(f"**Vraag:** {vraag}")
        st.markdown(f"**Antwoord:** {antwoord}")
        st.write("Was dit nuttig? 👍 👎")

def vraag_aan_groq(vraag, context):
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "llama3-70b-8192"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent een Nederlandse productspecialist bij Kastol. "
                        "Gebruik alleen de onderstaande context om te antwoorden. "
                        "Als je het antwoord niet zeker weet, geef dat dan eerlijk toe.

"
                        f"{context}"
                    ),
                },
                {"role": "user", "content": vraag},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Er ging iets mis met Groq API: {e}"
