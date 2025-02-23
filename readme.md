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
    <li>get_all_methods(): Retrieves all method codes from the database.</li>
    <li>generate_embedding(text): Uses Ollama’s embeddings API to create vectors.</li>
    <li>store_embeddings(): Loads existing embeddings, adds new ones, and saves the updated index.</li>
</ol>
Why Store Embeddings?
<ol>
    <li> Faster similarity searches.</li>
    <li>Precomputed embeddings enable quick retrieval.</li>
    <li> FAISS optimizes lookups for large datasets.</li>
<ol>
Step 3: Implementing retrieve_or_generate.py for Similar Unit Tests
This script finds the most similar method in the database and retrieves its unit test using FAISS and Ollama embeddings.

High-Level Steps
    <li>  User submits a method (string).
    <li>  Generate its embedding with Ollama.</li>
    <li>  Load the FAISS index.</li>
    <li>  Identify the most similar method via FAISS.</li>
    <li>  Retrieve its unit test from SQLite.</li>
Key Function
    <li>  get_unit_test_by_id(method_id): Fetches the unit test from SQLite.</li>
What retrieve_or_generate.py Does
    <li>  Embeds the input method.</li>
    <li> Finds the closest match in FAISS.</li>
    <li>  Returns the associated unit test.</li>
Step 4: Exposing retrieve_or_generate.py via API</li>
Added a /generate-test/ endpoint to testgen_api.py.

Example Request
```
curl -X POST "http://127.0.0.1:8000/generate-test/" -H "Content-Type: application/json" -d '{"language": "java", "method_code": "public int add(int a, int b) { return a + b; }"}'
```

<li> Returns a matching test if found.</li>
<li> Plans to auto-generate tests for unmatched methods (see Day 4).</li>