import discord

from utils import database_manager, database_scripts


async def on_settings(client: discord.Client, interaction: discord.Interaction) -> None:
    await database_scripts.check_create_settings(interaction.guild.id)

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
