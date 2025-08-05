import pandas as pd

def parse_excel(path):
    try:
        excel = pd.read_excel(path, sheet_name=None)
        output = []
        for sheet, df in excel.items():
            output.append(f"Tabblad: {sheet}")
            for _, row in df.iterrows():
                output.append(str(row.to_dict()))
        return "\n".join(output)
    except:
        return ""
