# My First LLM Using Ollama

## Day 1: Setting Up Ollama
Initially, I tried using OpenAI, but I ran into **quota limits**, so I switched to **Ollama** to run prompts **offline**.  
Since this was my **first LLM-based model**, I started with a **text-based** approach.  

Ollama runs **locally**, so **no API key is required**. 🚀  

---

## Installation  
You can install Ollama using **Homebrew** or download it manually:  

```sh
brew install ollama
```
Or download it from: [Ollama Downloads](https://ollama.com/download)  

### Verify Installation  
Check if Ollama is installed correctly:  
```sh
ollama --version
```

---

## Downloading Models  
Once installed, download models like:  
```sh
ollama pull mistral  # (~4.1 GB Download)
ollama pull llama2
```

---

## Running Ollama  
Start the Ollama service in the background:  
```sh
ollama serve
```
Verify if it's running:  
```sh
ollama list
```

---

## Switching to a Lighter Model  
Since **Mistral** was **too heavy (4.1 GB)** and took **~25.68 sec** to execute, I switched to **Gemma:2B**, which is **lighter and faster**.  

### Uninstall Mistral  
```sh
ollama rm mistral
```

### Install Gemma:2B  
```sh
ollama pull gemma:2b
```
With **Gemma:2B**, I got responses in **~0.50 sec**.  

---

## Testing with API  
Example API call:  
```sh
curl -X POST "http://127.0.0.1:8000/chat/"      -H "Content-Type: application/json"      -d '{"prompt": "Hello, how are you?"}'
```

📌 **Medium Post**: [Hello LLM: My First LLM Using Ollama](https://medium.com/@amanvaidya700/hello-llm-my-first-llm-using-ollama-b2e35b45ae49)  

---

# Day 2: Training the Model for Unit Test Generation  

## Step 1: Database Connectivity & Sample Data  
🔹 Connected to an **SQLite3 database** and inserted **sample method-test pairs** for **Java, Python, and JavaScript**.  
🔹 Initially, my prompt was handling only **one response before exiting**—fixed that!  

---

## Step 2: Generating & Storing Embeddings for Retrieval  
To enable **efficient test case retrieval**, we store method embeddings using **FAISS**.  

### Install FAISS or ChromaDB for Vector Storage  
```sh
pip install faiss-cpu chromadb numpy
```
📌 **If pip fails to install packages**, use:  
```sh
pip install faiss-cpu chromadb numpy --break-system-packages
```

---

### 📌 How `generate_embedding.py` Works  

1️⃣ **Fetch all methods** from the SQLite database.  
2️⃣ **Check if embeddings exist** in FAISS (avoid redundant embedding generation).  
3️⃣ **Generate embeddings** using **Ollama (Gemma 2)** for new methods.  
4️⃣ **Store embeddings** in a FAISS index (`faiss_index.bin`).  
5️⃣ **Update FAISS** only when **new methods** are added.  

---

### 🔍 Breakdown of Key Functions  

**1️⃣ `get_all_methods()`**  
🔹 Fetches **all method codes** from the database.  

**2️⃣ `generate_embedding(text)`**  
🔹 Calls Ollama’s **embeddings API** to generate vector representations.  

**3️⃣ `store_embeddings()`**  
🔹 Loads **existing embeddings** from FAISS.  
🔹 **Checks for new methods** and only embeds those.  
🔹 Saves the **updated FAISS index** for fast retrieval.  

---

### 📌 Why Store Embeddings?  

✅ **Faster search** instead of parsing every method manually.  
✅ **Precomputed embeddings** allow quick **similarity-based retrieval**.  
✅ **FAISS optimizes** lookup speeds for **large datasets**.  

---

## Step 3: Implementing `search.py` to Retrieve Similar Unit Tests  

This script **searches for the most similar method** in the database and **retrieves its corresponding unit test** using FAISS + Ollama embeddings.  

### 🔹 High-Level Steps  

1️⃣ **User provides a method** (as a string).  
2️⃣ **Generate an embedding** using Ollama.  
3️⃣ **Load the FAISS index** (precomputed method embeddings).  
4️⃣ **Find the most similar method** using FAISS.  
5️⃣ **Retrieve the corresponding unit test** from SQLite.  

---

### 🔍 Breakdown of `search.py` Functions  

**1️⃣ `get_unit_test_by_id(method_id)`**  
🔹 Fetches the **unit test** for the most similar method **from SQLite**.  

---

## 📌 What `search.py` Does  

✔ **Embeds** the new method using Ollama.  
✔ **Finds the most similar stored method** using FAISS.  
✔ **Fetches the corresponding unit test** from SQLite.  
✔ **Efficient search** using vector embeddings.  

---

## Step 4: Exposing `search.py` via an API Endpoint  

### Updated `api.py`
Now, we added a **new API endpoint** `/generate-test/` to fetch test cases.  

#### Example Request  
```sh
curl -X POST "http://127.0.0.1:8000/generate-test/"      -H "Content-Type: application/json"      -d '{"language": "java", "method_code": "public int add(int a, int b) { return a + b; }"}'
```

📌 If a **matching test case** is found, it returns the test.  
📌 If **no match is found**, we can **auto-generate** a test case using LLM.  

---

## Next Steps 🚀  

✅ **Step 1:** Set up SQLite DB + sample test cases.  
✅ **Step 2:** Store & retrieve method embeddings using FAISS.  
✅ **Step 3:** Implement search functionality for similar unit tests.  
✅ **Step 4:** Expose search via API.  
🔜 **Step 5:** Auto-generate test cases using Ollama when no match is found.  

Stay tuned for more updates! 🎯🚀  


# Day 3: Training & Exploring Fine-Tuning Options

Training the Model for Test Case Generation

Continued training the model by generating test cases using Ollama.

Ensured embeddings were properly stored and retrieved.

Attempting to Fine-Tune Ollama

Tried creating a Modelfile to fine-tune gemma:2b.

Encountered an error: Ollama does not support fine-tuning natively.

Since fine-tuning is required, we are now exploring external fine-tuning options.

Next Steps

🔹 Integrate Ollama with fine-tuning models like:

Axolotl (QLoRA-based fine-tuning)

Hugging Face’s PEFT + LoRA🔹 Continue generating test cases and refine retrieval.

Next Steps

✅ Step 1: Set up SQLite DB + sample test cases.✅ Step 2: Store & retrieve method embeddings using FAISS.✅ Step 3: Implement search functionality for similar unit tests.✅ Step 4: Expose search via API.✅ Step 5: Train model for test generation.🔜 Step 6: Fine-tune using external tools (Axolotl, Hugging Face PEFT).

Stay tuned for more updates!