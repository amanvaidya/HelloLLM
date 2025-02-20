import numpy as np
import faiss
import ollama
import os

VECTOR_DB_PATH = "faiss_index.idx"

def generate_embedding(text):
    response = ollama.embeddings(model="gemma:2b", prompt=text)
    
    # Ensure response contains 'embedding' key
    if "embedding" not in response:
        raise ValueError("Invalid embedding response from Ollama")
    
    embedding = np.array(response["embedding"], dtype=np.float32)
    print(f"Generated embedding shape: {embedding.shape}")  # Debugging info
    
    return embedding

def load_or_create_index(embedding_dim):
    if os.path.exists(VECTOR_DB_PATH):
        index = faiss.read_index(VECTOR_DB_PATH)
        print(f"Loaded existing FAISS index with dimension: {index.d}")
        
        # Ensure FAISS index matches embedding dimensions
        if index.d != embedding_dim:
            print("FAISS index dimension mismatch! Recreating index...")
            index = faiss.IndexFlatL2(embedding_dim)  # Recreate index with correct dimension
    else:
        print("Creating new FAISS index...")
        index = faiss.IndexFlatL2(embedding_dim)
    
    return index

def store_embeddings():
    sample_text = "public int add(int a, int b) { return a + b; }"  # Replace with actual method code
    embedding = generate_embedding(sample_text)

    # Load existing or create new FAISS index
    index = load_or_create_index(embedding.shape[0])

    index.add(np.array([embedding]))  # Add only new embeddings
    print("Embedding added successfully.")

    # Save updated FAISS index
    faiss.write_index(index, VECTOR_DB_PATH)
    print("FAISS index saved.")

if __name__ == "__main__":
    store_embeddings()