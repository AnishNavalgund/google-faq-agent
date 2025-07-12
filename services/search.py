import json
import numpy as np
from typing import List, Dict
from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput
import vertexai
import os
from dotenv import load_dotenv

load_dotenv()

vertexai.init(
    project=os.getenv("VERTEX_PROJECT_ID", "root-isotope-465710-h1"),
    location=os.getenv("VERTEX_LOCATION", "us-central1")
)

model = TextEmbeddingModel.from_pretrained("text-embedding-005")

# Load your embedded FAQ knowledge base
with open("data/faq_embeddings.json", "r") as f:
    EMBEDDINGS = json.load(f)

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search_faq(query: str, top_k: int = 1, threshold: float = 0.75) -> List[Dict]:
    """Returns the top_k most relevant FAQ entries for a user query"""
    embedding_input = TextEmbeddingInput(task_type="RETRIEVAL_QUERY", text=query)
    user_embedding = model.get_embeddings([embedding_input])[0].values

    scored = []
    for entry in EMBEDDINGS:
        score = cosine_similarity(user_embedding, entry["embedding"])
        if score >= threshold:
            scored.append({
                "question": entry["question"],
                "answer": entry["answer"],
                "score": round(score, 4)
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
