import discord

from utils import database_manager

async def on_guild_remove(client: discord.Client, guild: discord.Guild) -> None:
    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        await db.execute("DELETE FROM guilds WHERE guild_id = ?", guild.id)
        await db.commit()
    finally:
        await db.disconnect()
