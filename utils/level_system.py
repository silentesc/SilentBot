import discord
from datetime import datetime

from utils import database_manager, database_scripts


# TODO: Help for every level up replacement like {member_mention} etc.
# TODO: Add a way to disable xp gain for certain channels
# TODO: Add a way to disable xp gain for certain roles
# TODO: Add a way to disable xp gain for certain users


class LevelSystem:
    cooldown_members = {}

    @staticmethod
    async def trigger_xp_gain(guild: discord.Guild, member: discord.Member, message_channel: discord.TextChannel = None) -> None:
        await database_scripts.check_create_settings(guild.id)
        
        db = database_manager.SQLiteManager()
        await db.connect()

        # Get the settings for the guild
        settings_rows = await db.execute_one("SELECT leveling_enabled, xp_gain_cooldown_secs, xp_per_message, level_up_message_enabled, level_up_message, level_up_message_channel_id FROM settings WHERE guild_id = ?", guild.id)
        leveling_enabled: bool = bool(settings_rows[0])
        xp_gain_cooldown_secs: int = settings_rows[1]
        xp_per_message: int = settings_rows[2]
        level_up_message_enabled: bool = bool(settings_rows[3])
        level_up_message: str = settings_rows[4]
        level_up_message_channel_id: int = settings_rows[5]

        # Return if leveling is disabled
        if not leveling_enabled:
            return

        now = datetime.now().timestamp()

        # Check if guild and member are in cooldown_members dict
        if not LevelSystem.cooldown_members.get(guild.id):
            LevelSystem.cooldown_members[guild.id] = {}
        if not LevelSystem.cooldown_members[guild.id].get(member.id):
            LevelSystem.cooldown_members[guild.id][member.id] = 0
        
        # Check if the member is in cooldown
        cooldown = -(now - xp_gain_cooldown_secs - LevelSystem.cooldown_members[guild.id][member.id])
        if cooldown > 0:
            print(f"Member {member.id} is in cooldown for {cooldown} seconds")
            return
        LevelSystem.cooldown_members[guild.id][member.id] = now

        # Get the user's xp and level
        row = await db.execute_one("SELECT * FROM leveling WHERE guild_id = ? AND member_id = ?", guild.id, member.id)

        # Create new row or get from existing row
        if not row:
            await db.execute("INSERT INTO leveling (guild_id, member_id, xp, level) VALUES (?, ?, 0, 0)", guild.id, member.id)
            xp = 0
            level = 0
        else:
            xp = row[3]
            level = row[4]
        
        # Calculate the new xp and level
        leveled_up = False
        xp_needed_to_level_up = LevelSystem.get_xp_needed_to_level_up(level)
        xp += xp_per_message
        while xp >= xp_needed_to_level_up:
            leveled_up = True
            level += 1
            xp = xp - xp_needed_to_level_up
            xp_needed_to_level_up = LevelSystem.get_xp_needed_to_level_up(level)
        
        # Check if the user has leveled up
        if leveled_up:
            if level_up_message_enabled:
                channel = guild.get_channel(level_up_message_channel_id)
                if not channel and message_channel:
                    channel = message_channel
                
                if channel:
                    await channel.send(
                        level_up_message
                        .replace("{member_mention}", member.mention)
                        .replace("{member_name}", member.name)
                        .replace("{member_id}", str(member.id))
                        .replace("{level}", str(level))
                        .replace("{xp}", str(xp))
                    )
        
        # Update the user's xp and level
        await db.execute("UPDATE leveling SET xp = ?, level = ? WHERE guild_id = ? AND member_id = ?", xp, level, guild.id, member.id)
        await db.commit()
        await db.disconnect()


    @staticmethod
    def get_xp_needed_to_level_up(level: int) -> int:
        return 100 * (level + 1)
