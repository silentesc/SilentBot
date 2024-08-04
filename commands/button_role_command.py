import discord

from views import button_roles
from utils import database_manager


async def on_button_role(client: discord.Client, interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
    await interaction.response.defer()

    db = database_manager.SQLiteManager()
    await db.connect()

    try:
        custom_id = await db.execute_one("INSERT INTO button_roles (label, style, message_id, channel_id, role_id, guild_id) VALUES (?, ?, 0, ?, ?, ?) RETURNING id", label,  discord.ButtonStyle.primary.value, interaction.channel_id, role.id, interaction.guild_id)
        custom_id = custom_id[0]

        view = button_roles.ButtonRoles(label=label, custom_id=str(custom_id), style=discord.ButtonStyle.primary, role=role)

        sent_message = await interaction.channel.send(message_text, view=view)

        await db.execute("UPDATE button_roles SET message_id = ? WHERE id = ?", sent_message.id, custom_id)
        await db.commit()

        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            pass
    finally:
        await db.disconnect()
