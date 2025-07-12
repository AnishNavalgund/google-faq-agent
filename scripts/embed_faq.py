import os
import re
import json
from dotenv import load_dotenv

from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput
import vertexai

load_dotenv()
vertexai.init(project="root-isotope-465710-h1", location="us-central1")
model = TextEmbeddingModel.from_pretrained("text-embedding-005")

# Read and parse the FAQ text file
faq_path = "data/faq.txt"
with open(faq_path, "r") as f:
    content = f.read()

pairs = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=\nQ:|\Z)", content, re.DOTALL)
print(f"Found {len(pairs)} FAQ entries.")

faq_embeddings = []

for question, answer in pairs:
    embedding_input = TextEmbeddingInput(
        task_type="RETRIEVAL_QUERY", 
        text=question
    )
    embedding = model.get_embeddings([embedding_input])[0].values
    faq_embeddings.append({
        "question": question.strip(),
        "answer": answer.strip(),
        "embedding": embedding
    })

print("Generated embeddings using text-embedding-005.")

output_path = "data/faq_embeddings.json"
with open(output_path, "w") as f:
    json.dump(faq_embeddings, f, indent=2)

print(f"Saved embeddings to {output_path}")
