import ollama
import json
import os
import logging
import numpy as np
import faiss
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from threading import Lock
from config.settings import DB_PATH

logging.basicConfig(level=logging.INFO)

MODEL_NAME = "gemma:2b"
TRAINING_DATA_PATH = "training_data.jsonl"
EMBEDDING_DIR = "embeddings"
EMBEDDING_DATA_PATH = os.path.join(EMBEDDING_DIR, "training_data_embedding.jsonl")
INDEX_PATH = os.path.join(EMBEDDING_DIR, "faiss_index.idx")

def generate_embedding(item, index, total):
    prompt = item.get("prompt")
    try:
        embedding_response = ollama.embeddings(model=MODEL_NAME, prompt=prompt)
        embedding = np.array(embedding_response["embedding"], dtype=np.float32)
        item["embedding"] = embedding.tolist()
        logging.info(f"Processed new embedding for prompt {index+1}/{total}")
        return (item, embedding)
    except Exception as e:
        logging.error(f"Error generating embedding for prompt '{prompt}': {e}")
        return None

def store_embeddings(num_threads=4):
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

    # Identify prompts needing new embeddings
    new_items = [item for item in data if item.get("prompt") not in existing_embeddings]
    embeddings = [np.array(existing_embeddings[item["prompt"]]["embedding"], dtype=np.float32) 
                  for item in data if item["prompt"] in existing_embeddings]
    
    if not new_items:
        logging.info("No new embeddings to generate.")
    else:
        # Thread-safe collections
        result_queue = Queue()
        lock = Lock()

        # Generate embeddings in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_item = {executor.submit(generate_embedding, item, i, len(data)): i 
                            for i, item in enumerate(new_items)}
            
            for future in as_completed(future_to_item):
                result = future.result()
                if result:
                    item, embedding = result
                    result_queue.put((item, embedding))

        # Collect results
        new_data = []
        while not result_queue.empty():
            item, embedding = result_queue.get()
            new_data.append(item)
            embeddings.append(embedding)

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