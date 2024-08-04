import discord

from utils import database_manager


async def on_raw_reaction_add(client: discord.Client, raw_reaction: discord.RawReactionActionEvent) -> None:
    if raw_reaction.user_id == client.user.id:
        return
    
    user = client.get_user(raw_reaction.user_id)
    reaction_message_id = raw_reaction.message_id
    reaction_emoji = raw_reaction.emoji.name

    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        reaction_roles_rows = await db.execute_one("SELECT message_id, channel_id, role_id, emoji FROM reaction_roles WHERE message_id = ?", reaction_message_id)
        message_id = reaction_roles_rows[0]
        channel_id = reaction_roles_rows[1]
        role_id = reaction_roles_rows[2]
        emoji = reaction_roles_rows[3]

        if reaction_roles_rows is None:
            return
        if raw_reaction.message_id != message_id:
            return
        if reaction_emoji != emoji:
            return
        
        guild = client.get_guild(raw_reaction.guild_id)
        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        member = guild.get_member(user.id)
        role = guild.get_role(role_id)

        await message.remove_reaction(emoji, member)

        if role in member.roles:
            await member.remove_roles(role)
        else:
            await member.add_roles(role)
    finally:
        await db.disconnect()
