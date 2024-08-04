import datetime
import discord

from utils import database_manager


async def on_leaderboard(client: discord.Client, interaction: discord.Interaction) -> None:
    db = database_manager.SQLiteManager()
    await db.connect()
    rows = await db.execute("SELECT member_id, xp, level FROM leveling ORDER BY ((100 * (level + 1)) * level / 2 + xp) DESC LIMIT 10")
    await db.disconnect()

    leaderboard_msg = ""

    count = 0
    for row in rows:
        member = client.get_user(row[0])
        if not member:
            continue
        xp = row[1]
        level = row[2]
        leaderboard_msg += f"#{count + 1} - {member.mention} - Level {level} - {xp} XP\n"
    
    if not rows or not leaderboard_msg:
        await interaction.response.send_message("No one is on the leaderboard yet.")
        return

    embed = discord.Embed(
        title="Leaderboard",
        description=leaderboard_msg,
        color=0x98aaff,
    )

    await interaction.response.send_message(embed=embed)
