from discord import Intents, Message
from discord.ext import commands

from data.env import Env
from events import ready_event, message_event
from commands import help_command, ping_command
from utils import logger


class Bot:
    def __init__(self, env: Env) -> None:
        self.env = env
        self.intents = Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix=env.get_prefix(), intents=self.intents)
        self.bot.help_command = None

        """
        Events
        """

        @self.bot.event
        async def on_ready() -> None:
            await ready_event.on_ready(self.bot)
        
        @self.bot.event
        async def on_message(message: Message) -> None:
            # Check if the message is a command and process it, then return
            if message.content.startswith(self.env.get_prefix()):
                command_name = message.content.split(" ")[0].lower().replace(self.env.get_prefix(), "")
                if self.bot.get_command(command_name) is not None:
                    await self.bot.process_commands(message)
                    return
            
            # Call event
            await message_event.on_message(self.bot, message)
        
        @self.bot.event
        async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
            command_name = ctx.command.name
            command_author = ctx.author
            command_message_content = ctx.message.content

            error_message = f"{error}\nCommand Name: {command_name}\nAuthor: {command_author}\nMessage: {command_message_content}"
            logger.log_error(error_message)
        
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
