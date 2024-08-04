import discord

from utils import level_system


async def on_message(client: discord.Client, message: discord.Message) -> None:
    # Return if the message is from the bot itself
    if message.author == client.user:
        return
    
    guild = message.guild
    channel = message.channel
    author = message.author

    await level_system.trigger_xp_gain(guild, author, channel)
