import ollama

response = ollama.embeddings(model="gemma:2b", prompt="test")
print(response)