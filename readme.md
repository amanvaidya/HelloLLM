# My First LLM Using Ollama

## Day 1: Setting Up Ollama
I initially explored OpenAI but hit quota limits, so I pivoted to **Ollama** for offline prompt execution.  
As my first LLM-based project, I opted for a text-based approach.  

Ollama runs locally—no API key needed. 🚀  

---

### Installation  
Install Ollama via **Homebrew** or manually:  

```sh
brew install ollama

Or download from: <a href="https://ollama.com/download" target="_blank">Ollama Downloads</a>
```
Verify Installation
Confirm it’s working:
ollama --version

Downloading Models
Pull models like:
```
ollama pull mistral  # ~4.1 GB
ollama pull llama2
```

Running Ollama
Start the service in the background:
```
ollama serve
```
Check available models:
```
ollama list
```

Switching to a Lighter Model
Mistral (4.1 GB) was too slow (~25.68 sec), so I switched to Gemma:2B, which is lighter and faster (~0.50 sec).

Uninstall Mistral

```
ollama rm mistral
```

Install Gemma:2B
```
ollama pull gemma:2b
```
Testing with API
Sample API call:
```
curl -X POST "http://127.0.0.1:8000/chat/" -H "Content-Type: application/json" -d '{"prompt": "Hello, how are you?"}'
```
📌 Medium Post: <a href="https://medium.com/@amanvaidya700/hello-llm-my-first-llm-using-ollama-b2e35b45ae49">Hello LLM: My First LLM Using Ollama</a>


# Day 2: Training the Model for Unit Test Generation
Step 1: Database Connectivity & Sample Data
Connected to an SQLite3 database and added sample method-test pairs for Java, Python, and JavaScript.
Fixed an issue where my prompt exited after one response.

Step 2: Generating & Storing Embeddings for Retrieval
To enable efficient test case retrieval, I used FAISS to store method embeddings.

Install FAISS or ChromaDB
```
pip install faiss-cpu chromadb numpy
```
📌 If pip fails:
```
pip install faiss-cpu chromadb numpy --break-system-packages
```

How embed_methods.py Works
<ol>
   1. Fetch all methods from the SQLite database.
   2. Check if embeddings exist in FAISS to avoid redundancy.
   3. Generate embeddings for new methods using Ollama (Gemma:2B).
   4. Store embeddings in a FAISS index (faiss_index.bin).
   5. Update FAISS only for new methods.
</ol>
Key Functions
<ol>
    <li>1. get_all_methods(): Retrieves all method codes from the database.</li>
    <li>2. generate_embedding(text): Uses Ollama’s embeddings API to create vectors.</li>
    <li>3. store_embeddings(): Loads existing embeddings, adds new ones, and saves the updated index.</li>
</ol>
Why Store Embeddings?
<ol>
    1. Faster similarity searches.
    2. Precomputed embeddings enable quick retrieval.
    3. FAISS optimizes lookups for large datasets.
<ol>
Step 3: Implementing retrieve_or_generate.py for Similar Unit Tests
This script finds the most similar method in the database and retrieves its unit test using FAISS and Ollama embeddings.

High-Level Steps
    1. User submits a method (string).
    2. Generate its embedding with Ollama.
    3. Load the FAISS index.
    4. Identify the most similar method via FAISS.
    5. Retrieve its unit test from SQLite.
Key Function
    1. get_unit_test_by_id(method_id): Fetches the unit test from SQLite.
What retrieve_or_generate.py Does
    1. Embeds the input method.
    2. Finds the closest match in FAISS.
    3. Returns the associated unit test.
Step 4: Exposing retrieve_or_generate.py via API
Added a /generate-test/ endpoint to testgen_api.py.

Example Request
```
curl -X POST "http://127.0.0.1:8000/generate-test/" -H "Content-Type: application/json" -d '{"language": "java", "method_code": "public int add(int a, int b) { return a + b; }"}'
```

1. Returns a matching test if found.
2. Plans to auto-generate tests for unmatched methods (see Day 4).