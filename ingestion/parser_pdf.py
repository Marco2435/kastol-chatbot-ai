
import PyPDF2
from PIL import Image
import pytesseract
from utils.logger import get_logger

logger = get_logger("parser_pdf")

def parse_pdf(path):
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        logger.error(f"Fout bij parse_pdf bestand: {path} | {e}")
        return ""

def parse_pdf_ocr(image_path):
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang='nld')
    except Exception as e:
        logger.error(f"Fout bij OCR op afbeelding: {image_path} | {e}")
        return ""
