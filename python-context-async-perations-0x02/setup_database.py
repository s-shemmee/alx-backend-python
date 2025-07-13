import sqlite3

def setup_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table with age column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
    """)
    
    # Insert sample data
    users = [
        ('Alice', 'alice@example.com', 30),
        ('Bob', 'bob@example.com', 45),
        ('Charlie', 'charlie@example.com', 22),
        ('Diana', 'diana@example.com', 50)
    ]
    
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        users
    )
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_db()