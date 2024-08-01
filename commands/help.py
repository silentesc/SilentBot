from discord.ext import commands


async def help(ctx: commands.Context, *args) -> None:
    print(args)
