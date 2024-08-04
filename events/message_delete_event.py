import discord

from utils import database_manager


async def on_message_delete(client: discord.Client, message: discord.Message) -> None:
    if message.author.id == client.user.id:
        return

    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        await db.execute("DELETE FROM button_roles WHERE message_id = ?", message.id)
        await db.execute("DELETE FROM reaction_roles WHERE message_id = ?", message.id)
        await db.commit()
    finally:
        await db.disconnect()
