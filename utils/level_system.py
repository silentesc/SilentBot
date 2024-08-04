import discord
from utils import database_manager, database_scripts


# TODO: Add a cooldown for xp gain
# TODO: Help for every level up replacement like {member_mention} etc.
# TODO: Add a way to disable xp gain for certain channels
# TODO: Add a way to disable xp gain for certain roles
# TODO: Add a way to disable xp gain for certain users


async def trigger_xp_gain(guild: discord.Guild, author: discord.Member, message_channel: discord.TextChannel = None) -> None:
    await database_scripts.check_create_settings(guild.id)
    
    db = database_manager.SQLiteManager()
    await db.connect()

    # Get the settings for the guild
    settings_rows = await db.execute_one("SELECT leveling_enabled, xp_per_message, level_up_message_enabled, level_up_message, level_up_message_channel_id FROM settings WHERE guild_id = ?", guild.id)
    leveling_enabled: bool = bool(settings_rows[0])
    xp_per_message: int = settings_rows[1]
    level_up_message_enabled: bool = bool(settings_rows[2])
    level_up_message: str = settings_rows[3]
    level_up_message_channel_id: int = settings_rows[4]

    # Return if leveling is disabled
    if not leveling_enabled:
        return

    # Get the user's xp and level
    row = await db.execute_one("SELECT * FROM leveling WHERE guild_id = ? AND member_id = ?", guild.id, author.id)

    # Create new row or get from existing row
    if not row:
        await db.execute("INSERT INTO leveling (guild_id, member_id, xp, level) VALUES (?, ?, 0, 0)", guild.id, author.id)
        xp = 0
        level = 0
    else:
        xp = row[3]
        level = row[4]
    
    # Calculate the new xp and level
    leveled_up = False
    xp_needed_to_level_up = get_xp_needed_to_level_up(level)
    xp += xp_per_message
    while xp >= xp_needed_to_level_up:
        leveled_up = True
        level += 1
        xp = xp - xp_needed_to_level_up
        xp_needed_to_level_up = get_xp_needed_to_level_up(level)
    
    # Check if the user has leveled up
    if leveled_up:
        if level_up_message_enabled:
            channel = guild.get_channel(level_up_message_channel_id)
            if not channel and message_channel:
                channel = message_channel
            
            if channel:
                await channel.send(
                    level_up_message
                    .replace("{member_mention}", author.mention)
                    .replace("{member_name}", author.name)
                    .replace("{member_id}", str(author.id))
                    .replace("{level}", str(level))
                    .replace("{xp}", str(xp))
                )
    
    # Update the user's xp and level
    await db.execute("UPDATE leveling SET xp = ?, level = ? WHERE guild_id = ? AND member_id = ?", xp, level, guild.id, author.id)
    await db.commit()
    await db.disconnect()


def get_xp_needed_to_level_up(level: int) -> int:
    return 100 * (level + 1)
