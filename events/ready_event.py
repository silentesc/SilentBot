import discord

from utils import storage_manager
from views import reaction_roles


async def on_ready(client: discord.Client) -> None:
    # await self.tree.sync(guild=discord.Object(id=self.env.get_test_guild_id()))
    # await self.tree.sync()

    # Check if tables in db exist
    db = storage_manager.SQLiteManager()
    await db.connect()
    await db.execute("CREATE TABLE IF NOT EXISTS reaction_roles (id INTEGER PRIMARY KEY NOT NULL, label TEXT NOT NULL, style INTEGER NOT NULL, role_id INTEGER NOT NULL, guild_id INTEGER NOT NULL)")
    await db.commit()

    rows = await db.execute("SELECT * FROM reaction_roles")
    await db.disconnect()

    for row in rows:
        guild = await client.fetch_guild(row[4])
        role = discord.utils.get(guild.roles, id=row[3])

        view = reaction_roles.ReactionRoles(label=row[1], custom_id=str(row[0]), style=row[2], role=role)
        client.add_view(view)

    print("Logged on as", client.user)
