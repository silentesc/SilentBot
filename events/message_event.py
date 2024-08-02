from discord import Message
from discord.ext import commands


async def on_message(bot: commands.Bot, message: Message) -> None:
    # Return if the message is from the bot itself
    if message.author == bot.user:
        return
    
    print(f"Message from {message.author}: {message.content}")
