from discord.ext import commands


async def on_help(bot: commands.Bot, ctx: commands.Context, *args) -> None:
    print(args)
