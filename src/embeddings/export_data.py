import sqlite3
import json
from config.settings import DB_PATH

OUTPUT_FILE = "training_data.jsonl"

def export_training_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT language, method_code, test_code FROM method_tests")
    data = cursor.fetchall()
    conn.close()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for language, method_code, test_code in data:
            prompt = f"Write a unit test for this {language} method:\n{method_code}"
            response = test_code
            json.dump({"prompt": prompt, "response": response}, f)
            f.write("\n")

    print(f"✅ Training data exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_training_data()