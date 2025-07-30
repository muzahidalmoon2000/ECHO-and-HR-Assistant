from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cosine_similarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def rank_files_by_similarity(query, files, top_k=None):
    if not files:
        print("⚠️ No files to rank.")
        return []

    # Extract the best available content for each file (prefer full extracted text over just name)
    content_inputs = []
    filtered_files = []

    for f in files:
        text = f.get("extracted_text") or f.get("name")
        if not text or len(text.strip()) < 5:
            print(f"⚠️ Skipping {f.get('name', '[unnamed]')} — no usable text.")
            continue
        content_inputs.append(text[:2000])  # Truncate if needed
        filtered_files.append(f)

    if not filtered_files:
        print("⚠️ No valid files with extractable content.")
        return []

    try:
        query_embedding = client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"
        ).data[0].embedding

        content_embeddings = client.embeddings.create(
            input=content_inputs,
            model="text-embedding-3-small"
        ).data

    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return filtered_files  # Return unranked

    # Score and assign similarity
    for file, emb in zip(filtered_files, content_embeddings):
        file['similarity_score'] = cosine_similarity(query_embedding, emb.embedding)

    ranked = sorted(filtered_files, key=lambda x: x['similarity_score'], reverse=True)
    return ranked[:top_k] if top_k else ranked
