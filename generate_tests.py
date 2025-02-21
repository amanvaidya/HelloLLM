import sqlite3
import random
import string
from db.database import DB_PATH  # Ensure this file exists

# Supported programming languages
LANGUAGES = [
    "java", "python", "javascript", "c", "cpp", "csharp", "go", "rust", "kotlin", "swift", "scala", 
    "ruby", "php", "perl", "haskell", "elixir", "typescript", "bash", "powershell", "sql", "graphql"
]

# Test scenarios
SCENARIOS = [
    ("Arithmetic Operations", ["+", "-", "*", "/", "%"]),
    ("String Manipulation", ["concat", "reverse", "toUpperCase", "toLowerCase"]),
    ("Array/List Operations", ["sort", "reverse", "findMax", "findMin"]),
    ("File Handling", ["readFile", "writeFile", "deleteFile"]),
    ("Database Operations", ["insertRecord", "fetchRecord", "deleteRecord"]),
    ("Null Checks", ["handleNull"]),
    ("Exception Handling", ["throwException", "catchException"]),
    ("Concurrency", ["threadSafety", "asyncExecution"]),
    ("Mock-Based Tests", ["mockService", "mockRepository"])
]

# Check if a method already exists in the database
def method_exists(cursor, language, method_code):
    cursor.execute("SELECT 1 FROM method_tests WHERE language = ? AND method_code = ?", (language, method_code))
    return cursor.fetchone() is not None

# Generate a unique method name
def random_method_name(existing_methods):
    while True:
        name = ''.join(random.choices(string.ascii_lowercase, k=6))
        if name not in existing_methods:
            existing_methods.add(name)
            return name

# Generate method code
def generate_method_code(language, method_name, scenario):
    operation = random.choice(["+", "-", "*", "/", "%"])
    
    code_map = {
        "java": f"public int {method_name}(int a, int b) {{ return a {operation} b; }}",
        "python": f"def {method_name}(a, b): return a {operation} b",
        "javascript": f"function {method_name}(a, b) {{ return a {operation} b; }}",
        "c": f"int {method_name}(int a, int b) {{ return a {operation} b; }}",
        "cpp": f"int {method_name}(int a, int b) {{ return a {operation} b; }}",
        "csharp": f"public int {method_name}(int a, int b) {{ return a {operation} b; }}",
        "go": f"func {method_name}(a int, b int) int {{ return a {operation} b }}",
        "rust": f"fn {method_name}(a: i32, b: i32) -> i32 {{ a {operation} b }}",
        "swift": f"func {method_name}(a: Int, b: Int) -> Int {{ return a {operation} b }}",
        "ruby": f"def {method_name}(a, b) a {operation} b end",
        "php": f"function {method_name}($a, $b) {{ return $a {operation} $b; }}",
        "bash": f"{method_name}() {{ echo $(( $1 {operation} $2 )) }}",
    }
    return code_map.get(language, "")

# Generate test cases
def generate_test_code(language, method_name):
    if language == "java":
        return f"""import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
public class {method_name.capitalize()}Test {{
    @Test public void test{method_name.capitalize()}() {{
        assertEquals(5, new Calculator().{method_name}(2, 3));
    }}
}}"""

    elif language == "python":
        return f"""import unittest
class Test{method_name.capitalize()}(unittest.TestCase):
    def test_{method_name}(self):
        self.assertEqual({method_name}(2, 3), 5)
if __name__ == '__main__':
    unittest.main()"""

    elif language == "javascript":
        return f"""const assert = require('assert');
describe('{method_name}', function() {{
    it('should return correct result', function() {{
        assert.strictEqual({method_name}(2, 3), 5);
    }});
}});"""
    
    return ""

# Insert 80,000 unique test cases
def insert_bulk_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    existing_methods = set()
    batch_size = 5000
    total_inserted = 0

    cursor.execute("SELECT method_code FROM method_tests")
    for row in cursor.fetchall():
        existing_methods.add(row[0].split(" ")[2])  # Extract method name

    print(f"✅ Existing methods loaded: {len(existing_methods)}")

    for _ in range(80000):
        language = random.choice(LANGUAGES)
        scenario, _ = random.choice(SCENARIOS)
        method_name = random_method_name(existing_methods)
        method_code = generate_method_code(language, method_name, scenario)
        test_code = generate_test_code(language, method_name)

        if method_code and not method_exists(cursor, language, method_code):
            cursor.execute("INSERT INTO method_tests (language, method_code, test_code) VALUES (?, ?, ?)", 
                           (language, method_code, test_code))
            total_inserted += 1

            if total_inserted % batch_size == 0:
                conn.commit()
                print(f"✅ {total_inserted} test cases inserted...")

    conn.commit()
    conn.close()
    print(f"🚀 Successfully inserted {total_inserted} unique test cases!")

if __name__ == "__main__":
    insert_bulk_data()