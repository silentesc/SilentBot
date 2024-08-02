import discord

from data.env import Env
from events import ready_event, message_event
from commands import help_command, ping_command


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
        Commands
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


    def run(self):
        self.client.run(self.env.get_token())
