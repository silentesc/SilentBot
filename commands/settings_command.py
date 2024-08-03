import discord

from utils import database_manager, database_scripts


async def on_settings(client: discord.Client, interaction: discord.Interaction, setting: str = None, new_value: str = None) -> None:
    await database_scripts.check_create_settings(interaction.guild.id)

    # If no setting provided, show all settings
    if not setting:
        db = database_manager.SQLiteManager()
        await db.connect()
        rows = await db.execute_one("SELECT * FROM settings WHERE guild_id = ?", interaction.guild.id)
        await db.disconnect()
        
        msg = ""
        msg += f"leveling_enabled: `{bool(rows[2])}`\n"
        msg += f"xp_per_message: `{rows[3]}`\n"
        msg += f"level_up_message_enabled: `{bool(rows[4])}`\n"
        msg += f"level_up_message: `{rows[5]}`\n"
        msg += f"level_up_message_channel_id: `{rows[6]}`\n"

        response_embed = discord.Embed(
            title="Settings",
            color=0x98aaff,
            description=msg
        )

        await interaction.response.send_message(embed=response_embed)
        return
    
    # Check user permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You must be an administrator to change settings.", ephemeral=True)
        return
    
    # If setting provided but no new value, return
    if not new_value:
        await interaction.response.send_message("You must provide a new value.", ephemeral=True)
        return
    
    # If setting provided and new value, update setting
    db = database_manager.SQLiteManager()
    await db.connect()
    match setting:
        case "leveling_enabled":
            if new_value.lower() not in ["true", "false"]:
                await interaction.response.send_message("Invalid value. Please provide `true` or `false`.", ephemeral=True)
                return
            await db.execute("UPDATE settings SET leveling_enabled = ? WHERE guild_id = ?", new_value.lower() == "true", interaction.guild.id)
        case "xp_per_message":
            if not new_value.isdigit():
                await interaction.response.send_message("Invalid value. Please provide a number.", ephemeral=True)
                return
            await db.execute("UPDATE settings SET xp_per_message = ? WHERE guild_id = ?", new_value, interaction.guild.id)
        case "level_up_message_enabled":
            if new_value.lower() not in ["true", "false"]:
                await interaction.response.send_message("Invalid value. Please provide `true` or `false`.", ephemeral=True)
                return
            await db.execute("UPDATE settings SET level_up_message_enabled = ? WHERE guild_id = ?", new_value.lower() == "true", interaction.guild.id)
        case "level_up_message":
            await db.execute("UPDATE settings SET level_up_message = ? WHERE guild_id = ?", new_value, interaction.guild.id)
        case "level_up_message_channel_id":
            if not new_value.isdigit():
                await interaction.response.send_message("Invalid value. Please provide a number.", ephemeral=True)
                return
            channel_id = int(new_value)
            try:
                await client.fetch_channel(channel_id)
            except discord.errors.NotFound:
                await interaction.response.send_message("Channel not found. Please provide a valid channel ID.", ephemeral=True)
                return
            await db.execute("UPDATE settings SET level_up_message_channel_id = ? WHERE guild_id = ?", new_value, interaction.guild.id)
        case _:
            await interaction.response.send_message("Invalid setting.", ephemeral=True)
            return
    
    await db.commit()
    await db.disconnect()
    await interaction.response.send_message("Setting updated.", ephemeral=True)
