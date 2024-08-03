import aiosqlite


db_path = "data/database.db"


class SQLiteManager:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await aiosqlite.connect(db_path)

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def execute(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            return await cursor.fetchall()

    async def execute_one(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            return await cursor.fetchone()

    async def execute_many(self, query, values):
        async with self.connection.executemany(query, values) as cursor:
            return await cursor.fetchall()

    async def commit(self):
        await self.connection.commit()

    async def rollback(self):
        await self.connection.rollback()


async def check_create_tables():
    db = SQLiteManager()
    await db.connect()

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS button_roles (
            id INTEGER PRIMARY KEY NOT NULL,
            label TEXT NOT NULL,
            style INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL
        )
        """
    )

    await db.commit()
    await db.disconnect()
