import discord

from utils import database_manager

async def on_guild_join(client: discord.Client, guild: discord.Guild) -> None:
    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", guild.id)
        await db.commit()
    finally:
        await db.disconnect()
