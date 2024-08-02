import discord
import os


async def on_help(client: discord.Client, interaction: discord.Interaction, command: str) -> None:
    title = "Help"
    help_page = None

    if not command:
        with open("help/general_help.txt", "r") as file:
            help_page = file.read()
    else:
        title = f"Help for `{command}`"
        path = f"help/specific_help/{command}.txt"

        if not os.path.exists(path):
            await interaction.response.send_message(f"Help for command `{command}` not found.")
            return

        with open(path, "r") as file:
            help_page = file.read()
    
    response_embed = discord.Embed(
        title=title,
        description=help_page,
        color=0x98aaff
    )

    await interaction.response.send_message(embed=response_embed)
