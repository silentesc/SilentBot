from discord import Intents
from discord.ext import commands

from data.env import Env
from events import ready_event
from commands import help_command, ping_command


class Bot:
    def __init__(self, env: Env) -> None:
        self.env = env
        self.intents = Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix="?", intents=self.intents)
        self.bot.help_command = None

        """
        Events
        """

        @self.bot.event
        async def on_ready() -> None:
            await ready_event.on_ready(self.bot)
        
        """
        Commands
        """

        @self.bot.command(name="help")
        async def help(ctx: commands.Context, *args) -> None:
            await help_command.on_help(self.bot, ctx, *args)
        
        @self.bot.command(name="ping")
        async def ping(ctx: commands.Context, *args) -> None:
            await ping_command.on_ping(self.bot, ctx, *args)


    def run(self):
        self.bot.run(self.env.get_token())
