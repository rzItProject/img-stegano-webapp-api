import asyncio
import asyncpg


DB_CONFIG = "postgresql://postgres:&*SuperRootSQL$@localhost:5432/test"

async def test_connection():
    conn = None
    try:
        conn = await asyncpg.connect(DB_CONFIG)
        print("Successfully connected to the database!")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        if conn:
            await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(test_connection())