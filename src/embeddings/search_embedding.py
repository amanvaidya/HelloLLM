import faiss
import numpy as np
import ollama
import logging
import sqlite3
from config.settings import DB_PATH

logging.basicConfig(level=logging.INFO)

INDEX_PATH = "embeddings/faiss_index.idx"
SIMILARITY_THRESHOLD = 0.6

def generate_embedding(text: str) -> np.ndarray:
    response = ollama.embeddings(model="gemma:2b", prompt=text)
    return np.array(response["embedding"], dtype=np.float32)

def fetch_test_code(index: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT test_code FROM method_tests WHERE id = ?", (index + 1,))  # Assuming IDs start at 1
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def search_similar_method(method_code: str):
    logging.info("Generating embedding for search query...")
    query_embedding = generate_embedding(method_code).reshape(1, -1)
    
    logging.info("Loading FAISS index...")
    if not os.path.exists(INDEX_PATH):
        logging.error(f"FAISS index not found at {INDEX_PATH}")
        return None
    index = faiss.read_index(INDEX_PATH)
    
    logging.info("Searching for similar embeddings...")
    distances, indices = index.search(query_embedding, k=1)
    
    logging.info(f"Search results - Distance: {distances[0][0]}, Index: {indices[0][0]}")
    
    if distances[0][0] < SIMILARITY_THRESHOLD:
        test_code = fetch_test_code(indices[0][0])
        if test_code:
            logging.info("Similar test case found.")
            return test_code
        else:
            logging.warning("Test case not found in database.")
            return None
    else:
        logging.warning("No similar test case found.")
        return None

if __name__ == "__main__":
    test_method = "public int add(int a, int b) { return a + b; }"
    result = search_similar_method(test_method)
    print("Result:", result)