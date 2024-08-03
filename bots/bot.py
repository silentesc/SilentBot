import discord

from data.env import Env
from events import ready_event, message_event
from commands import help_command, ping_command, button_role_command, settings_command
from utils import logger


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
            # await self.tree.sync(guild=discord.Object(id=self.env.get_test_guild_id()))
            # await self.tree.sync()

            await ready_event.on_ready(self.client)

        
        @self.client.event
        async def on_message(message: discord.Message) -> None:
            await message_event.on_message(self.client, message)
        
        """
        Slash Commands
        """

        # Help Command
        @self.tree.command(
            name="help",
            description="Displays help about commands.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.choices(command=[
            discord.app_commands.Choice(name="help", value="help"),
            discord.app_commands.Choice(name="ping", value="ping"),
            discord.app_commands.Choice(name="button_role", value="button_role"),
            discord.app_commands.Choice(name="settings", value="settings"),
        ])
        async def help(interaction: discord.Interaction, command: discord.app_commands.Choice[str] = None) -> None:
            command_value = command.value if command else None
            await help_command.on_help(self.client, interaction, command_value)
        

        # Ping Command
        @self.tree.command(
            name="ping",
            description="Displays the bots reponse time und latency.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        async def ping(interaction: discord.Interaction) -> None:
            await ping_command.on_ping(self.client, interaction)
        

        # Button Role Command
        @self.tree.command(
            name="button_role",
            description="Creates a button that assigns a role to the user.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.bot_has_permissions(manage_roles=True)
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def button_role(interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
            await button_role_command.on_button_role(self.client, interaction, message_text, label, role)
        

        # Settings Command
        @self.tree.command(
            name="settings",
            description="Displays the server's settings.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        async def settings(interaction: discord.Interaction) -> None:
            await settings_command.on_settings(self.client, interaction)

        """
        Slash Command Error Handling
        """

        @self.tree.error
        async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
            logger.log_error(error)
            await interaction.response.send_message(f"{error}", ephemeral=True)


    def run(self):
        self.client.run(self.env.get_token())
