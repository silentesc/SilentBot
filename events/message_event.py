import discord

from utils import database_manager, database_scripts


async def on_message(client: discord.Client, message: discord.Message) -> None:
    # Return if the message is from the bot itself
    if message.author == client.user:
        return
    
    guild = message.guild
    author = message.author

    db = database_manager.SQLiteManager()
    await db.connect()
    row = await db.execute_one("SELECT * FROM leveling WHERE guild_id = ? AND member_id = ?", guild.id, author.id)

    # If the user is not in the database, add them
    if not row:
        await db.execute("INSERT INTO leveling (guild_id, member_id, xp, level) VALUES (?, ?, 0, 0)", guild.id, author.id)
        await db.commit()
        await db.disconnect()
        return
    
    xp = row[3]
    level = row[4]
    xp_needed_to_level_up = 100 * (level + 1)

    # Add xp and check if the user has leveled up
    settings_rows = await database_scripts.get_settings(guild.id)
    xp += settings_rows[3]

    if xp >= xp_needed_to_level_up:
        level += 1
        xp = 0
        await message.channel.send(f"{author.mention} has leveled up to level {level}!")
    
    # Update the user's xp and level
    await db.execute("UPDATE leveling SET xp = ?, level = ? WHERE guild_id = ? AND member_id = ?", xp, level, guild.id, author.id)
    await db.commit()
    await db.disconnect()
