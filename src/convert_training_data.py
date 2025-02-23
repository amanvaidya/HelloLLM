import json

INPUT_FILE = "training_data.jsonl"
OUTPUT_FILE = "fine_tune_data.txt"

with open(INPUT_FILE, "r", encoding="utf-8") as infile, open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        prompt = data["prompt"]
        response = data["response"]
        # Write in Ollama-compatible format
        outfile.write(f"<|system|>You are a unit test generator.<|user|>{prompt}<|assistant}>{response}\n")
    print(f"Converted training data to {OUTPUT_FILE}")