
import os
import streamlit as st
from .parser_pdf import parse_pdf
from .parser_docx import parse_docx
from .parser_excel import parse_excel
from .parser_csv import parse_csv
from .parser_html import parse_html
from .parser_json import parse_json

@st.cache_data(show_spinner=False)
def load_all_files(folder="data"):
    content = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            content.append(parse_pdf(path))
        elif file.endswith(".docx"):
            content.append(parse_docx(path))
        elif file.endswith(".xlsx"):
            content.append(parse_excel(path))
        elif file.endswith(".csv"):
            content.append(parse_csv(path))
        elif file.endswith(".html") or file.endswith(".htm"):
            content.append(parse_html(path))
        elif file.endswith(".json"):
            content.append(parse_json(path))
    return "\n".join(content)

def load_uploaded_files(uploaded_files):
    content = []
    for file in uploaded_files:
        name = file.name.lower()
        if name.endswith(".pdf"):
            content.append(parse_pdf(file))
        elif name.endswith(".docx"):
            content.append(parse_docx(file))
        elif name.endswith(".xlsx"):
            content.append(parse_excel(file))
        elif name.endswith(".csv"):
            content.append(parse_csv(file))
        elif name.endswith(".html") or name.endswith(".htm"):
            content.append(parse_html(file))
        elif name.endswith(".json"):
            content.append(parse_json(file))
    return "\n".join(content)

def route_all_files(folder="data"):
    blocks = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            tekst = parse_pdf(path)
        elif file.endswith(".docx"):
            tekst = parse_docx(path)
        elif file.endswith(".xlsx"):
            tekst = parse_excel(path)
        elif file.endswith(".csv"):
            tekst = parse_csv(path)
        elif file.endswith(".html") or file.endswith(".htm"):
            tekst = parse_html(path)
        elif file.endswith(".json"):
            tekst = parse_json(path)
        else:
            tekst = ""
        if tekst:
            blocks.extend(tekst.split("\n\n"))
    return blocks
