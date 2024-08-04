import discord


async def on_raw_reaction_add(client: discord.Client, raw_reaction: discord.RawReactionActionEvent) -> None:
    if raw_reaction.user_id == client.user.id:
        return
    
    emoji = "👍"
    print(raw_reaction.message_id)
    print(raw_reaction.emoji.name, raw_reaction.emoji.name == emoji)
