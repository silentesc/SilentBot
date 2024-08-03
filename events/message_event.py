import discord

from utils import database_manager, database_scripts


async def on_message(client: discord.Client, message: discord.Message) -> None:
    # Return if the message is from the bot itself
    if message.author == client.user:
        return
    
    guild = message.guild
    author = message.author

    await database_scripts.check_create_settings(guild.id)
    
    db = database_manager.SQLiteManager()
    await db.connect()
    settings_rows = await db.execute_one("SELECT leveling_enabled, xp_per_message, level_up_message_enabled, level_up_message, level_up_message_channel_id FROM settings WHERE guild_id = ?", guild.id)
    leveling_enabled: bool = bool(settings_rows[0])
    xp_per_message: int = settings_rows[1]
    level_up_message_enabled: bool = bool(settings_rows[2])
    level_up_message: str = settings_rows[3]
    level_up_message_channel_id: int = settings_rows[4]

    # Return if leveling is disabled
    if not leveling_enabled:
        return

    row = await db.execute_one("SELECT * FROM leveling WHERE guild_id = ? AND member_id = ?", guild.id, author.id)

    # If the user is not in the database, add them
    if not row:
        await db.execute("INSERT INTO leveling (guild_id, member_id, xp, level) VALUES (?, ?, ?, 0)", guild.id, author.id, xp_per_message)
        await db.commit()
        await db.disconnect()
        return
    
    xp = row[3]
    level = row[4]
    xp_needed_to_level_up = 100 * (level + 1)

    # Add xp and check if the user has leveled up
    xp += xp_per_message
    if xp >= xp_needed_to_level_up:
        level += 1
        xp = 0
        if level_up_message_enabled:
            channel = guild.get_channel(level_up_message_channel_id)
            if not channel:
                channel = message.channel
            
            await channel.send(
                level_up_message
                .replace("{member_mention}", author.mention)
                .replace("{member_name}", author.name)
                .replace("{member_id}", str(author.id))
                .replace("{level}", str(level))
                .replace("{xp}", str(xp))
                .replace("{xp_needed_to_level_up}", str(xp_needed_to_level_up))
                .replace("{guild_name}", guild.name)
                .replace("{guild_id}", str(guild.id))
            )
    
    # Update the user's xp and level
    await db.execute("UPDATE leveling SET xp = ?, level = ? WHERE guild_id = ? AND member_id = ?", xp, level, guild.id, author.id)
    await db.commit()
    await db.disconnect()
