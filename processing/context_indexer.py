import faiss
import os
import pickle
import numpy as np
from groq_api import get_embedding
from processing.context_cleaner import clean_context

index_path = "logs/faiss.index"
meta_path = "logs/metadata.pkl"

def maak_semantische_index(documenten):
    embeddings = []
    metadata = []

    for doc in documenten:
        schone_tekst = clean_context(doc.get("inhoud", ""))
        vector = get_embedding(schone_tekst)
        embeddings.append(vector)
        metadata.append({
            "inhoud": schone_tekst,
            "merk": doc.get("merk", ""),
            "model": doc.get("model", ""),
            "type": doc.get("type", ""),
            "afmetingen": doc.get("afmetingen", ""),
            "referentie": doc.get("referentie", "")
        })

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

def zoek_relevante_context(vraag, topk=3):
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return []

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    vraag_vector = get_embedding(vraag)
    vraag_vector = np.array([vraag_vector]).astype('float32')

    D, I = index.search(vraag_vector, topk)
    resultaten = []

    for i in I[0]:
        if i < len(metadata):
            item = metadata[i]
            resultaten.append(
                f"{item['merk']} {item['model']} {item['type']} {item['afmetingen']} -> Referentie: {item['referentie']}"
            )

    return "\n".join(resultaten)
