import ollama
import json
import os
import logging
import numpy as np
import faiss
import sqlite3
from config.settings import DB_PATH

logging.basicConfig(level=logging.INFO)

MODEL_NAME = "gemma:2b"  # Using base Gemma:2b as no adapter is specified
TRAINING_DATA_PATH = "training_data.jsonl"
EMBEDDING_DIR = "embeddings"
EMBEDDING_DATA_PATH = os.path.join(EMBEDDING_DIR, "training_data_embedding.jsonl")
INDEX_PATH = os.path.join(EMBEDDING_DIR, "faiss_index.idx")

def store_embeddings():
    # Ensure directories exist
    os.makedirs(EMBEDDING_DIR, exist_ok=True)

    # Load training data
    if not os.path.exists(TRAINING_DATA_PATH):
        logging.error(f"Training data file not found: {TRAINING_DATA_PATH}")
        return
    with open(TRAINING_DATA_PATH, "r") as f:
        data = [json.loads(line) for line in f]
    logging.info(f"Loaded {len(data)} training samples.")

    # Load existing embeddings
    existing_embeddings = {}
    if os.path.exists(EMBEDDING_DATA_PATH):
        with open(EMBEDDING_DATA_PATH, "r") as f:
            existing_data = json.load(f)
            existing_embeddings = {item["prompt"]: item for item in existing_data}
        logging.info(f"Loaded {len(existing_embeddings)} existing embeddings.")

    # Generate embeddings for new data
    new_data = []
    embeddings = []
    for i, item in enumerate(data):
        prompt = item.get("prompt")
        if prompt in existing_embeddings:
            embeddings.append(np.array(existing_embeddings[prompt]["embedding"], dtype=np.float32))
            continue

        try:
            embedding_response = ollama.embeddings(model=MODEL_NAME, prompt=prompt)
            embedding = np.array(embedding_response["embedding"], dtype=np.float32)
            item["embedding"] = embedding.tolist()
            new_data.append(item)
            embeddings.append(embedding)
            logging.info(f"Processed new embedding for prompt {i+1}/{len(data)}")
        except Exception as e:
            logging.error(f"Error generating embedding for prompt '{prompt}': {e}")

    # Merge and save embeddings
    final_data = list(existing_embeddings.values()) + new_data
    with open(EMBEDDING_DATA_PATH, "w") as f:
        json.dump(final_data, f, indent=4)
    logging.info(f"Saved {len(final_data)} embeddings to {EMBEDDING_DATA_PATH}")

    # Build and save FAISS index
    if embeddings:
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))
        faiss.write_index(index, INDEX_PATH)
        logging.info(f"FAISS index created and saved at {INDEX_PATH}")

if __name__ == "__main__":
    store_embeddings()