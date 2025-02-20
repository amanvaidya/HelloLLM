import sqlite3
import faiss
import numpy as np
import ollama
import os
from database import DB_PATH  # Import DB path

VECTOR_DB_PATH = "faiss_index.bin"

def get_all_methods():
    """Fetch all method_code entries from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, method_code FROM method_tests")
    methods = cursor.fetchall()
    conn.close()
    return methods  # List of (id, method_code)

def generate_embedding(text):
    """Generate an embedding for the given text using Ollama."""
    response = ollama.embeddings(model="gemma:2", prompt=text)
    return np.array(response["embedding"], dtype="float32")  # Ensure float32 format for FAISS

def store_embeddings():
    """Generate and store embeddings in FAISS, updating only for new methods."""
    methods = get_all_methods()

    if not methods:
        print("No methods found in the database.")
        return

    dimension = 4096  # Adjust based on Gemma output size

    # Load existing FAISS index or create a new one
    if os.path.exists(VECTOR_DB_PATH):
        index = faiss.read_index(VECTOR_DB_PATH)
        existing_count = index.ntotal  # Existing embeddings count
    else:
        index = faiss.IndexFlatL2(dimension)
        existing_count = 0

    method_ids = []
    new_methods = methods[existing_count:]  # Only get new methods

    if not new_methods:
        print("No new embeddings to store.")
        return

    for method_id, method_code in new_methods:
        embedding = generate_embedding(method_code)
        index.add(np.array([embedding]))  # Add only new embeddings
        method_ids.append(method_id)

    faiss.write_index(index, VECTOR_DB_PATH)  # Save updated FAISS index
    print(f"Stored {len(new_methods)} new embeddings.")

if __name__ == "__main__":
    store_embeddings()