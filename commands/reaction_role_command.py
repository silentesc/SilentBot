import discord

from views import reaction_roles
from utils import storage_manager


async def on_reaction_role(client: discord.Client, interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
    db = storage_manager.SQLiteManager()
    await db.connect()
    custom_id = await db.execute_one("INSERT INTO reaction_roles (label, style, role_id, guild_id) VALUES (?, ?, ?, ?) RETURNING id", label,  discord.ButtonStyle.primary.value, role.id, interaction.guild_id)
    await db.commit()
    await db.disconnect()

    view = reaction_roles.ReactionRoles(label=label, custom_id=str(custom_id[0]), style=discord.ButtonStyle.primary, role=role)

    await interaction.response.send_message(message_text, view=view)
