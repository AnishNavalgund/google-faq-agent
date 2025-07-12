import json
import numpy as np
from dotenv import load_dotenv
from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput
import vertexai

load_dotenv()
vertexai.init(project="root-isotope-465710-h1", location="us-central1")

model = TextEmbeddingModel.from_pretrained("text-embedding-005")

with open("data/faq_embeddings.json", "r") as f:
    faq_data = json.load(f)

def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

user_question = input("Ask a question: ").strip()

embedding_input = TextEmbeddingInput(
    task_type="RETRIEVAL_QUERY",
    text=user_question
)

user_embedding = model.get_embeddings([embedding_input])[0].values

best_match = None
best_score = -1

for entry in faq_data:
    score = cosine_similarity(user_embedding, entry["embedding"])
    if score > best_score:
        best_score = score
        best_match = entry

print("\nBest Match:")
print("Q:", best_match["question"])
print("A:", best_match["answer"])
print(f"Similarity Score: {best_score:.4f}")
