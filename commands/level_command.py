import discord

from utils import database_manager


async def on_level(client: discord.Client, interaction: discord.Interaction, member: discord.Member = None) -> None:
    if not member:
        member = interaction.user

    db = database_manager.SQLiteManager()
    await db.connect()
    row = await db.execute_one("SELECT xp, level FROM leveling WHERE guild_id = ? AND member_id = ?", interaction.guild_id, member.id)
    await db.disconnect()

    if not row:
        await interaction.response.send_message("This user has no level yet.")
        return
    
    xp = row[0]
    level = row[1]
    xp_needed_to_level_up = 100 * (level + 1)
    progress_percent = round((xp / xp_needed_to_level_up) * 100, 2)
    progress_bar = "█" * int(progress_percent / 10) + "▁" * int(10 - progress_percent / 10)

    response_embed = discord.Embed(
        title=f"{member.name}'s Level",
        description=f"**Level:** {level}\n**XP**: {xp}",
        color=0x98aaff,
    )
    response_embed.set_author(name=member.name, icon_url=member.avatar)
    response_embed.add_field(name="Progress", value=f"{progress_bar} {progress_percent}%", inline=False)

    await interaction.response.send_message(embed=response_embed)
