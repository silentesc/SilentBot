import discord

from utils import database_scripts


async def on_settings(client: discord.Client, interaction: discord.Interaction) -> None:
    rows = database_scripts.get_settings(interaction.guild.id)
    
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
