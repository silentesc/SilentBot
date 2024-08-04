import discord

from utils import database_manager, database_scripts
from views import button_roles


async def on_ready(client: discord.Client) -> None:
    # Create tables if they do not exist
    await database_scripts.check_create_tables()

    # Load buttons from the database
    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        rows = await db.execute("SELECT * FROM button_roles")
        for row in rows:
            guild = client.get_guild(row[4])
            role = discord.utils.get(guild.roles, id=row[3])
            view = button_roles.ButtonRoles(label=row[1], custom_id=str(row[0]), style=row[2], role=role)
            client.add_view(view)

        # Bot is ready
        print("Logged on as", client.user)
    finally:
        await db.disconnect()
