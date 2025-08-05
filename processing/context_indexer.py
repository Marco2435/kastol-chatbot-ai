
import faiss
import os
import pickle
from groq_api import get_embedding
from processing.context_cleaner import clean_context

index_path = "logs/faiss.index"
meta_path = "logs/metadata.pkl"

def maak_semantische_index(documenten):
    embeddings = []
    metadata = []

    for doc in documenten:
        schone_tekst = clean_context(doc)
        vector = get_embedding(schone_tekst)
        embeddings.append(vector)
        metadata.append(schone_tekst)

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
    resultaten = [metadata[i] for i in I[0] if i < len(metadata)]

    return "\n".join(resultaten)
