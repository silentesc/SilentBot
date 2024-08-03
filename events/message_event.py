import discord


async def on_message(client: discord.Client, message: discord.Message) -> None:
    # Return if the message is from the bot itself
    if message.author == client.user:
        return
    
    guild = message.guild
    author = message.author

    
