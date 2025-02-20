import sqlite3
from db.database import DB_PATH  # Import database path

def method_exists(cursor, language, method_code):
    """Check if a method already exists in the database."""
    cursor.execute("SELECT 1 FROM method_tests WHERE language = ? AND method_code = ?", (language, method_code))
    return cursor.fetchone() is not None  # Returns True if the method exists

def insert_sample_data():
    """Inserts sample method-test pairs for different languages into the database if they don't already exist."""
    data = [
        ("java", 
         "public int add(int a, int b) { return a + b; }",
         """import static org.junit.jupiter.api.Assertions.*;
            import org.junit.jupiter.api.Test;
            public class CalculatorTest {
                @Test public void testAdd() {
                    Calculator calculator = new Calculator();
                    assertEquals(5, calculator.add(2, 3));
                }
            }"""),

        ("python", 
         "def add(a, b): return a + b",
         """import unittest
            class TestCalculator(unittest.TestCase):
                def test_add(self):
                    self.assertEqual(add(2, 3), 5)
            if __name__ == '__main__':
                unittest.main()"""),

        ("javascript", 
         "function add(a, b) { return a + b; }",
         """const assert = require('assert');
            describe('Calculator', function() {
                it('should add two numbers', function() {
                    assert.strictEqual(add(2, 3), 5);
                });
            });""")
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for language, method_code, test_code in data:
        if not method_exists(cursor, language, method_code):  # Insert only if it doesn't exist
            cursor.execute("INSERT INTO method_tests (language, method_code, test_code) VALUES (?, ?, ?)", 
                           (language, method_code, test_code))
            print(f"Inserted: {language} method")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_sample_data()