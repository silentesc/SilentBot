from discord import Intents
from discord.ext import commands

from data.env import Env
from events import ready
from commands import help


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
            await ready.on_ready(self.bot)
        
        """
        Commands
        """

        @self.bot.command(name="help")
        async def help(ctx: commands.Context, *args) -> None:
            await help.help(ctx, *args)


    def run(self):
        self.bot.run(self.env.get_token())
