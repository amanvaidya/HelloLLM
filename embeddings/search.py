import faiss
import numpy as np
import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

INDEX_PATH = "embeddings/faiss_index.idx"
SIMILARITY_THRESHOLD = 0.6  # Reduced from 0.8 to 0.6

def generate_embedding(text: str) -> np.ndarray:
    response = ollama.embeddings(model="gemma:2b", prompt=text)
    return np.array(response["embedding"], dtype=np.float32)

def search_similar_method(method_code: str):
    logging.info("Generating embedding for search query...")
    query_embedding = generate_embedding(method_code).reshape(1, -1)
    
    logging.info("Loading FAISS index...")
    index = faiss.read_index(INDEX_PATH)
    
    logging.info("Searching for similar embeddings...")
    distances, indices = index.search(query_embedding, k=1)  # Get closest match
    
    logging.info(f"Search results - Distance: {distances}, Indices: {indices}")
    
    if distances[0][0] < SIMILARITY_THRESHOLD:
        logging.info("Similar test case found, fetching...")
        # Fetch and return the stored test case (implement retrieval logic)
        return "Mock Test Case: Similar test case found."
    else:
        logging.warning("No similar test case found.")
        return None