import sys
import os
from src.db.database import create_database
from src.generators.sample_data import insert_sample_data
from src.generators.data_generator import insert_bulk_data
from src.embeddings.export_data import export_training_data
from src.embeddings.train_embedding import store_embeddings
from src.api.app import app as fastapi_app
import uvicorn

def run_full_setup(run_api=True):
    """Runs the entire project setup from database creation to FAISS index generation."""
    print("Starting full project setup...")
    
    # Step 1: Create the database
    print("Creating database...")
    create_database()

    # Step 2: Insert sample data
    print("Inserting sample data...")
    insert_sample_data()

    # Step 3: Insert bulk data (80,000 test cases)
    print("Inserting bulk data (this may take a while)...")
    insert_bulk_data(total_cases=1)

    # Step 4: Export data to JSONL
    print("Exporting training data to JSONL...")
    export_training_data()

    # Step 5: Generate embeddings and FAISS index
    print("Generating embeddings and FAISS index...")
    store_embeddings()

    print("Full setup complete!")

    # Step 6: Optionally start the FastAPI server
    if run_api:
        print("Starting FastAPI server...")
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Check for optional command-line argument to skip API
    run_api = "--no-api" not in sys.argv
    run_full_setup(run_api=run_api)