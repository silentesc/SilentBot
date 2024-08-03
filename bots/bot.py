import discord

from data.env import Env
from events import ready_event, message_event
from commands import help_command, ping_command, reaction_role_command
from utils import logger
from views import reaction_roles


class Bot:
    def __init__(self, env: Env) -> None:
        self.env = env
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.tree = discord.app_commands.CommandTree(self.client)

        """
        Events
        """

        @self.client.event
        async def on_ready() -> None:
            await ready_event.on_ready(self.client)

        
        @self.client.event
        async def on_message(message: discord.Message) -> None:
            await message_event.on_message(self.client, message)
        
        """
        Slash Commands
        """

        @self.tree.command(
            name="help",
            description="Displays help about commands.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.choices(command=[
            discord.app_commands.Choice(name="ping", value="ping"),
            discord.app_commands.Choice(name="help", value="help")
        ])
        async def help(interaction: discord.Interaction, command: discord.app_commands.Choice[str] = None) -> None:
            command_value = command.value if command else None
            await help_command.on_help(self.client, interaction, command_value)
        

        @self.tree.command(
            name="ping",
            description="Displays the bots reponse time und latency.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        async def ping(interaction: discord.Interaction) -> None:
            await ping_command.on_ping(self.client, interaction)
        

        @self.tree.command(
            name="reaction_role",
            description="Creates a button that assigns a role to the user.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.bot_has_permissions(manage_messages=True)
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def reaction_role(interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
            await reaction_role_command.on_reaction_role(self.client, interaction, message_text, label, role)
        

        """
        Slash Command Error Handling
        """

        # TODO
        # @self.tree.error
        # async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        #     logger.log_error(error)
        #     await interaction.response.send_message(f"{error}", ephemeral=True)


    def run(self):
        self.client.run(self.env.get_token())
