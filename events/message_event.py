from discord import Message
from discord.ext import commands


async def on_message(bot: commands.Bot, message: Message) -> None:
    print(f"Message from {message.author}: {message.content}")
