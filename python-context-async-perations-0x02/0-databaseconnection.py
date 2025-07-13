import sqlite3

class DatabaseConnection:
    """Custom context manager for database connections"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        
    def __enter__(self):
        """Open connection when entering context"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context"""
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

if __name__ == "__main__":
    # Example usage
    with DatabaseConnection('users.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("All users:", results)