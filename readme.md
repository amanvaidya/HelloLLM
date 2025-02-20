My First LLM using Ollama

Tried with OpenAI, but was getting quota expired, so downloaded Ollama to run prompts offline. 
Since it was my first LLM-based model, I was trying for a text-based model only.

Since Ollama installs locally, no API key is required.

## Installation

You can install Ollama using Homebrew or download it directly:

```sh
brew install ollama
```

Or download from: [https://ollama.com/download](https://ollama.com/download)

## Verify Installation

Check if Ollama is installed correctly:

```sh
ollama --version
```

## Downloading Models

Once installed, you can download models like:

```sh
ollama pull mistral  # (4.1 GB Download)
ollama pull llama2
```

## Running Ollama

Start the Ollama service in the background:

```sh
ollama serve
```

Verify if it's running:

```sh
ollama list
```

## Switching to a Lighter Model

Since Mistral was heavy (4.1 GB) and took **25.68 sec** to execute, I moved to a lighter model: **Gemma:2B**.

### Uninstall Mistral

```sh
ollama rm mistral
```

### Install Gemma:2B

```sh
ollama pull gemma:2b
```

Using **Gemma:2B**, I received a response in **0.50 sec**.

Sample Curl:
curl -X POST "http://127.0.0.1:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?"}'

Medium Post: https://medium.com/@amanvaidya700/hello-llm-my-first-llm-using-ollama-b2e35b45ae49

Day-2 Update:
Thought, why not train my model to generate unit test cases? 
Step 1: DB Connectivity and sample data insertion
Connected it to an SQLite3 DB and inserted some data. 
It is not a very big set just one line for java, python and js
Initially, my prompt was handling only one response before exiting—fixed that too!

Step 2: Generate and Store Embeddings for Retrieval
Install FAISS or ChromaDB for vector storage:
```
pip3.12 install faiss-cpu chromadb numpy
```
***Browine point if your system is also not installing packages using pip use --break-system-packages in the end
```
pip3.12 install faiss-cpu chromadb numpy --break-system-packages
```

break up of generate_embedding.py:
🔹 How It Works (Step by Step)
	1.	Fetch all method codes from method_tests table in SQLite.
	2.	Check if embeddings already exist (stored in FAISS).
	3.	Generate embeddings using Ollama (Gemma 2) for new methods.
	4.	Store these embeddings in a FAISS index (faiss_index.bin).
	5.	Update the FAISS index only if new methods are added (prevents regenerating embeddings every time the app starts).
📝 Breakdown of Key Functions

1️⃣ get_all_methods()
	•	Fetches all method IDs and their code from the database.

2️⃣ generate_embedding(text)
	•	Calls Ollama’s embeddings() API to generate a vector representation of the method code.

3️⃣ store_embeddings()
	•	Loads existing embeddings from FAISS (if available).
	•	Checks if new methods exist and only embeds new ones.
	•	Saves the updated FAISS index for retrieval later.
📌 Why is This Needed?
	•	Storing embeddings makes searching fast instead of parsing every method manually.
	•	Precomputed embeddings allow retrieval using similarity search.
	•	FAISS optimizes lookup speed for large datasets.

Next Step: Implement search.py to Retrieve Similar Unit Tests

Complete Breakdown of search.py
This script searches for the most similar method in the database and returns the corresponding unit test using FAISS and Ollama embeddings.

🔹 High-Level Steps
	1.	User provides a new method (as a string).
	2.	Generate an embedding for the method using Ollama.
	3.	Load the FAISS index (precomputed embeddings of stored methods).
	4.	Find the most similar stored method using FAISS.
	5.	Retrieve the corresponding unit test from SQLite.
📌 Function Breakdown

1️⃣ get_unit_test_by_id(method_id)
	•	Fetches the unit test from the SQLite database for a given method_id.

📌 What This Script Does

✔ Embeds the new method using Ollama
✔ Finds the most similar stored method using FAISS
✔ Fetches the corresponding unit test from SQLite
✔ Efficient search using vector embeddings