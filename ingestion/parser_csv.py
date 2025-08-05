import pandas as pd

def parse_csv(path):
    try:
        df = pd.read_csv(path)
        output = []
        for _, row in df.iterrows():
            output.append(str(row.to_dict()))
        return "\n".join(output)
    except:
        return ""
