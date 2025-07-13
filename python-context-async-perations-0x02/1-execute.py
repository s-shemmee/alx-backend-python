import sqlite3

class ExecuteQuery:
    """Reusable query context manager"""
    
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        
    def __enter__(self):
        """Execute query when entering context"""
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources"""
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    # Example usage
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as cursor:
        results = cursor.fetchall()
        print("Users over 25:", results)