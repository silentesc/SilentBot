import discord

from views import button_roles
from utils import database_manager


async def on_button_role(client: discord.Client, interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
    await interaction.response.defer()

    db = database_manager.SQLiteManager()
    await db.connect()
    custom_id = await db.execute_one("INSERT INTO button_roles (label, style, role_id, guild_id) VALUES (?, ?, ?, ?) RETURNING id", label,  discord.ButtonStyle.primary.value, role.id, interaction.guild_id)
    await db.commit()
    await db.disconnect()

    view = button_roles.ButtonRoles(label=label, custom_id=str(custom_id[0]), style=discord.ButtonStyle.primary, role=role)

    await interaction.channel.send(message_text, view=view)
    await interaction.delete_original_response()
