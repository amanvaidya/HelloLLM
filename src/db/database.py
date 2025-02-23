import sqlite3
from config.settings import DB_PATH

def create_database():
    """Creates the SQLite database and the method_tests table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS method_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            method_code TEXT NOT NULL,
            test_code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def method_exists(cursor, language, method_code):
    """Check if a method already exists in the database."""
    cursor.execute("SELECT 1 FROM method_tests WHERE language = ? AND method_code = ?", (language, method_code))
    return cursor.fetchone() is not None

if __name__ == "__main__":
    create_database()