from discord.ext import commands


async def on_ready(bot: commands.Bot) -> None:
    print("Logged on as", bot.user)
