import sqlite3
import json

DB_PATH = "unit_tests.db"  # Update if needed
OUTPUT_FILE = "training_data.jsonl"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch all test cases
cursor.execute("SELECT language, method_code, test_code FROM method_tests")
data = cursor.fetchall()
conn.close()

# Convert to JSONL format
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for language, method_code, test_code in data:
        prompt = f"Write a unit test for this {language} method:\n{method_code}"
        response = test_code
        json.dump({"prompt": prompt, "response": response}, f)
        f.write("\n")  # Newline for JSONL format

print(f"✅ Training data exported to {OUTPUT_FILE}")