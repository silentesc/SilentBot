import discord

from views import reaction_roles


async def on_reaction_role(client: discord.Client, interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
    view = reaction_roles.ReactionRoles(label=label, style=discord.ButtonStyle.primary, role=role)
    await interaction.response.send_message(message_text, view=view)
