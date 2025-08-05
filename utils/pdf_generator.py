
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def maak_chat_pdf(chatgeschiedenis, bestandsnaam='chatgeschiedenis.pdf'):
    c = canvas.Canvas(bestandsnaam, pagesize=A4)
    width, height = A4
    marge = 2 * cm
    regel_hoogte = 14
    y = height - marge

    c.setFont("Helvetica", 11)
    for item in chatgeschiedenis:
        if y < marge:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - marge

        regel = f"{item.get('rol', 'onbekend')}: {item.get('inhoud', '')}"
        regels = c.beginText(marge, y)
        regels.textLines(regel)
        c.drawText(regels)
        y -= (regel_hoogte * len(regel.splitlines())) + 5

    c.save()
