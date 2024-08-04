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
        button_roles_rows = await db.execute("SELECT id, label, style, message_id, channel_id, role_id, guild_id FROM button_roles")
        for row in button_roles_rows:
            id = row[0]
            label = row[1]
            style = row[2]
            message_id = row[3]
            channel_id = row[4]
            role_id = row[5]
            guild_id = row[6]

            guild = client.get_guild(guild_id)
            role = discord.utils.get(guild.roles, id=role_id)
            view = button_roles.ButtonRoles(label=label, custom_id=str(id), style=style, role=role)
            client.add_view(view)

            try:
                await guild.get_channel(channel_id).fetch_message(message_id)
            except discord.NotFound:
                await db.execute("DELETE FROM button_roles WHERE id = ?", id)
        await db.commit()
            
        
        reaction_roles_rows = await db.execute("SELECT id, message_id, channel_id, role_id, guild_id FROM reaction_roles")
        for row in reaction_roles_rows:
            id = row[0]
            message_id = row[1]
            channel_id = row[2]
            role_id = row[3]
            guild_id = row[4]

            guild = client.get_guild(guild_id)
            try:
                await guild.get_channel(channel_id).fetch_message(message_id)
            except discord.NotFound:
                await db.execute("DELETE FROM reaction_roles WHERE id = ?", id)
        await db.commit()

        # Bot is ready
        print("Logged on as", client.user)
    finally:
        await db.disconnect()
