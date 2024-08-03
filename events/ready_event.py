import discord

from utils import storage_manager
from views import button_roles


async def on_ready(client: discord.Client) -> None:
    # Check if tables in db exist
    db = storage_manager.SQLiteManager()
    await db.connect()
    await db.execute("CREATE TABLE IF NOT EXISTS button_roles (id INTEGER PRIMARY KEY NOT NULL, label TEXT NOT NULL, style INTEGER NOT NULL, role_id INTEGER NOT NULL, guild_id INTEGER NOT NULL)")
    await db.commit()

    rows = await db.execute("SELECT * FROM button_roles")
    await db.disconnect()

    for row in rows:
        guild = await client.fetch_guild(row[4])
        role = discord.utils.get(guild.roles, id=row[3])

        view = button_roles.ButtonRoles(label=row[1], custom_id=str(row[0]), style=row[2], role=role)
        client.add_view(view)

    print("Logged on as", client.user)
