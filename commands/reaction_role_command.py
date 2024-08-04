import discord

from utils import database_manager


async def on_reaction_role(client: discord.Client, interaction: discord.Interaction, message_text: str, emoji: str, role: discord.Role) -> None:
    await interaction.response.defer()

    db = database_manager.SQLiteManager()
    await db.connect()

    # Insert the reaction roles into the database
    try:
        id = await db.execute_one(
            "INSERT INTO reaction_roles (message_id, channel_id, role_id, guild_id) VALUES (0, ?, ?, ?) RETURNING id",
            interaction.channel_id,
            role.id,
            interaction.guild_id
        )
        id = id[0]

        sent_message = await interaction.channel.send(message_text)
        # Try to add the reaction to the message
        try:
            await sent_message.add_reaction(emoji)
        except discord.HTTPException:
            await db.execute("DELETE FROM reaction_roles WHERE id = ?", id)
            await db.commit()
            try:
                await sent_message.delete()
            except discord.NotFound:
                pass
            await interaction.response.send_message("Failed to add reaction to message, please use known emoji.", ephemeral=True)
            return

        await db.execute("UPDATE reaction_roles SET message_id = ? WHERE id = ?", sent_message.id, id)
        await db.commit()

        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            pass
    finally:
        await db.disconnect()
