import sqlite3
import faiss
import numpy as np
import ollama
from db.database import DB_PATH  # Import SQLite DB path
from generate_embedding import VECTOR_DB_PATH  # FAISS index path

def get_unit_test_by_id(method_id):
    """Fetch unit test code from SQLite by method ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT test_code FROM method_tests WHERE id = ?", (method_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def generate_embedding(text):
    """Generate an embedding for the given method using Ollama."""
    response = ollama.embeddings(model="gemma:2", prompt=text)
    return np.array(response["embedding"], dtype="float32")

def search_similar_method(method_code, top_k=1):
    """Find the most similar method and return its unit test."""
    # Load FAISS index
    index = faiss.read_index(VECTOR_DB_PATH)

    # Generate embedding for the input method
    query_embedding = generate_embedding(method_code).reshape(1, -1)

    # Search for the most similar method (top_k=1)
    distances, indices = index.search(query_embedding, top_k)

    # Get the best match's ID
    best_match_id = indices[0][0]

    if best_match_id == -1:
        print("No relevant test found.")
        return None

    # Fetch and return the corresponding unit test
    return get_unit_test_by_id(best_match_id)

if __name__ == "__main__":
    # Example search
    new_method = "def multiply(a, b): return a * b"
    result = search_similar_method(new_method)

    if result:
        print("Closest matching unit test:\n", result)
    else:
        print("No similar unit test found.")