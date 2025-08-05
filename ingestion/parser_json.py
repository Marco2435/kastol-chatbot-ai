import json

def parse_json(path):
    def flatten(d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        flat = flatten(data)
        return "\n".join([f"{k}: {v}" for k, v in flat.items()])
    except:
        return ""
