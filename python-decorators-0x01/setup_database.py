import sqlite3

def setup_test_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Drop table if exists
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
    """)
    
    # Insert test data
    cursor.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        [('Alice', 'alice@example.com'), 
         ('Bob', 'bob@example.com')]
    )
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_test_db()