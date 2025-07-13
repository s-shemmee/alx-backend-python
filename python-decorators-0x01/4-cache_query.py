import sqlite3
import functools

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        print("Executing and caching query")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    print("First run (executes query):")
    print(fetch_users_with_cache(query="SELECT * FROM users"))
    print("\nSecond run (uses cache):")
    print(fetch_users_with_cache(query="SELECT * FROM users"))