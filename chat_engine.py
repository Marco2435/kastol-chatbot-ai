
import streamlit as st
import os
import pandas as pd
import pytesseract
from PIL import Image
import PyPDF2
import docx
import io
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def lees_pdf(pad):
    tekst = ""
    try:
        with open(pad, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for pagina in reader.pages:
                inhoud = pagina.extract_text()
                if inhoud:
                    tekst += inhoud + "\n"
                else:
                    xobj = pagina.get("/Resources", {}).get("/XObject", {})
                    for obj in xobj:
                        if xobj[obj].get("/Subtype") == "/Image":
                            raw_data = xobj[obj].get_data()
                            img = Image.open(io.BytesIO(raw_data))
                            tekst += pytesseract.image_to_string(img, lang="nld")
    except Exception as e:
        tekst += f"\n[Fout bij PDF lezen: {e}]"
    return tekst

def laad_excel_data(pad="data"):
    resultaten = []
    for bestand in os.listdir(pad):
        if bestand.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(pad, bestand))
            resultaten.append(df)
    return pd.concat(resultaten, ignore_index=True) if resultaten else pd.DataFrame()

def zoek_excel(df, vraag):
    vraag_lower = vraag.lower()
    matches = df[df.apply(lambda rij: vraag_lower in str(rij).lower(), axis=1)]
    if not matches.empty:
        return matches.to_string(index=False)
    return "Geen directe match gevonden in Excel."

def laad_overige_context(pad="data"):
    context = []
    for bestand in os.listdir(pad):
        volledig_pad = os.path.join(pad, bestand)
        if bestand.endswith(".pdf"):
            context.append(lees_pdf(volledig_pad))
        elif bestand.endswith(".txt"):
            context.append(lees_txt(volledig_pad))
        elif bestand.endswith(".docx"):
            context.append(lees_docx(volledig_pad))
        elif bestand.lower().endswith(('.png', '.jpg', '.jpeg')):
            context.append(ocr_afbeelding(volledig_pad))
    return "\n".join(context)

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

def vraag_aan_groq(vraag, extra_context):
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "llama3-70b-8192"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Je bent een Nederlandse productspecialist bij Kastol. "
                        "Beantwoord de vraag op basis van onderstaande context. "
                        "Gebruik geen informatie die niet in de context staat. "
                        "Als iets niet zeker is, geef dat dan aan.\n\n"
                        f"{extra_context}"
                    ),
                },
                {"role": "user", "content": vraag},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Er ging iets mis met Groq API: {e}"

def run_chat():
    st.title("Kastol AI Chatbot 🤖")
    vraag = st.text_input("Wat wil je weten over een product of document?", "")
    if vraag:
        st.info("Even geduld, ik zoek het voor je uit...")

        df = laad_excel_data("data")
        excel_resultaat = zoek_excel(df, vraag)
        overige_context = laad_overige_context("data")

        antwoord = vraag_aan_groq(f"{vraag}\n\nExcel-resultaat:
{excel_resultaat}", overige_context)

        st.markdown(f"**Vraag:** {vraag}")
        st.markdown(f"**Antwoord:** {antwoord}")
        st.write("Was dit nuttig? 👍 👎")
