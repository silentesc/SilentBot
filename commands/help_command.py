import discord
from discord.ext import commands
import os


async def on_help(bot: commands.Bot, ctx: commands.Context, *args) -> None:
    title = "Help"
    help_page = None

    if len(args) == 0:
        with open("help/general_help.txt", "r") as file:
            help_page = file.read()
    else:
        title = f"Help for `{args[0]}`"
        path = f"help/specific_help/{args[0]}.txt"

        if not os.path.exists(path):
            await ctx.send(f"Help for command `{args[0]}` not found.")
            return

        with open(path, "r") as file:
            help_page = file.read()
    
    response_embed = discord.Embed(
        title=title,
        description=help_page,
        color=0x98aaff
    )

    await ctx.send(embed=response_embed)
