
from fpdf import FPDF
from datetime import datetime
import os

def maak_chat_pdf(geschiedenis, taal='NL'):
    datum = datetime.now().strftime("%Y-%m-%d_%H-%M")
    bestandsnaam = f"chat_Kastol_{datum}.pdf"
    pad = os.path.join("logs", bestandsnaam)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Kastol AI Chatbot - Gespreksverslag", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    for item in geschiedenis:
        tijd = item.get("tijd", "")
        vraag = item.get("vraag", "")
        antwoord = item.get("antwoord", "")
        pdf.multi_cell(0, 10, txt=f"🕓 {tijd}
Vraag: {vraag}
Antwoord: {antwoord}
", border=0)
        pdf.ln(3)

    pdf.output(pad)
    return pad
