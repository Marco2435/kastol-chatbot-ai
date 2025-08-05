import os
from .parser_pdf import parse_pdf
from .parser_docx import parse_docx
from .parser_json import parse_json
from .parser_csv import parse_csv
from .parser_excel import parse_excel
from .parser_html import parse_html

def route_all_files(bestanden):
    content = []
    for bestand in bestanden:
        extensie = os.path.splitext(bestand)[-1].lower()
        if extensie == ".pdf":
            content.append(parse_pdf(bestand))
        elif extensie == ".docx":
            content.append(parse_docx(bestand))
        elif extensie == ".json":
            content.append(parse_json(bestand))
        elif extensie == ".csv":
            content.append(parse_csv(bestand))
        elif extensie == ".xlsx":
            content.append(parse_excel(bestand))
        elif extensie == ".html":
            content.append(parse_html(bestand))
        else:
            content.append(f"Onbekend bestandstype: {bestand}")
    return "\n".join([str(c) if not isinstance(c, str) else c for c in content])

def load_all_files(mapnaam="data"):
    bestanden = []
    for root, _, files in os.walk(mapnaam):
        for file in files:
            bestanden.append(os.path.join(root, file))
    return route_all_files(bestanden)

def load_uploaded_files(uploaded_files):
    content = []
    for file in uploaded_files:
        extensie = os.path.splitext(file.name)[-1].lower()
        if extensie == ".pdf":
            content.append(parse_pdf(file))
        elif extensie == ".docx":
            content.append(parse_docx(file))
        elif extensie == ".json":
            content.append(parse_json(file))
        elif extensie == ".csv":
            content.append(parse_csv(file))
        elif extensie == ".xlsx":
            content.append(parse_excel(file))
        elif extensie == ".html":
            content.append(parse_html(file))
        else:
            content.append(f"Onbekend bestandstype: {file.name}")
    return "\n".join([str(c) if not isinstance(c, str) else c for c in content])