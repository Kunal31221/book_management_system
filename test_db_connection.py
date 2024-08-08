# test_db_connection.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "mysql+aiomysql://root:Sandhya@localhost/mydatabase"

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.connect() as conn:
        result = await conn.execute("SELECT 1")
        print(result.fetchall())

if __name__ == "__main__":
    asyncio.run(test_connection())
