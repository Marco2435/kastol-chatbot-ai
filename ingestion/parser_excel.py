import pandas as pd

def parse_excel(file_path):
    df = pd.read_excel(file_path)
    resultaten = []

    for _, row in df.iterrows():
        merk = str(row.get("Merk", "")).strip()
        model = str(row.get("Model", "")).strip()
        type_ = str(row.get("Type", "")).strip()
        lengte = str(row.get("Lengte", "")).strip()
        hoogte = str(row.get("Hoogte", "")).strip()
        referentie = str(row.get("Referentie", "")).strip()

        afmetingen = f"{lengte}x{hoogte}"
        inhoud = f"De referentie van {merk} {model} {type_} {afmetingen} is {referentie}"

        resultaten.append({
            "merk": merk,
            "model": model,
            "type": type_,
            "afmetingen": afmetingen,
            "referentie": referentie,
            "inhoud": inhoud
        })

    return resultaten
