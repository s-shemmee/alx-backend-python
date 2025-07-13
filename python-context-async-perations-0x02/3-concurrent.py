import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Run both queries concurrently"""
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    # Run the concurrent queries
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Users over 40:", older_users)