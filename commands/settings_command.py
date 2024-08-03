import discord

from utils import database_manager, database_scripts


async def on_settings(client: discord.Client, interaction: discord.Interaction) -> None:
    db = database_manager.SQLiteManager()
    await db.connect()
    rows = await db.execute_one("SELECT * FROM settings WHERE guild_id = ?", interaction.guild.id)
    await db.disconnect()

    if not rows:
        await database_scripts.insert_default_guild_settings(interaction.guild.id)
        print("Settings added")
        await on_settings(client, interaction)
        return
    
    leveling_enabled = bool(rows[2])
    xp_per_message = rows[3]
    level_up_message_enabled = bool(rows[4])
    level_up_message = rows[5]
    level_up_message_channel_id = rows[6]

    msg = ""
    msg += f"leveling_enabled: `{leveling_enabled}`\n"
    msg += f"xp_per_message: `{xp_per_message}`\n"
    msg += f"level_up_message_enabled: `{level_up_message_enabled}`\n"
    msg += f"level_up_message: `{level_up_message}`\n"
    msg += f"level_up_message_channel_id: `{level_up_message_channel_id}`\n"

    response_embed = discord.Embed(
        title="Settings",
        color=0x98aaff,
        description=msg
    )

    await interaction.response.send_message(embed=response_embed)
