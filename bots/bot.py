import discord

from data.env import Env
from events import ready_event, message_event
from commands import help_command, ping_command, button_role_command, settings_command
from utils import database_manager, database_scripts,logger


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
        Slash Commands for settings
        """
        

        # leveling_enabled Command
        @self.tree.command(
            name="leveling_enabled",
            description="Toggle leveling_enabled on or off.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def leveling_enabled(interaction: discord.Interaction) -> None:
            await database_scripts.check_create_settings(interaction.guild_id)
            
            db = database_manager.SQLiteManager()
            await db.connect()

            leveling_enabled = await db.execute_one("SELECT leveling_enabled FROM settings WHERE guild_id = ?", interaction.guild.id)
            leveling_enabled = leveling_enabled[0]
            if leveling_enabled:
                await db.execute("UPDATE settings SET leveling_enabled = 0")
                await interaction.response.send_message("Leveling has been disabled.")
            else:
                await db.execute("UPDATE settings SET leveling_enabled = 1")
                await interaction.response.send_message("Leveling has been enabled.")
            
            await db.commit()
            await db.disconnect()

        # xp_per_message Command
        @self.tree.command(
            name="xp_per_message",
            description="Set the value of xp_per_message.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def xp_per_message(interaction: discord.Interaction, xp: int) -> None:
            await database_scripts.check_create_settings(interaction.guild_id)

            db = database_manager.SQLiteManager()
            await db.connect()
            await db.execute("UPDATE settings SET xp_per_message = ? WHERE guild_id = ?", xp, interaction.guild.id)
            await db.commit()
            await db.disconnect()

            await interaction.response.send_message(f"xp_per_message has been set to `{xp}`.")

        # level_up_message_enabled Command
        @self.tree.command(
            name="level_up_message_enabled",
            description="Toggle level_up_message_enabled on or off.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def level_up_message_enabled(interaction: discord.Interaction) -> None:
            await database_scripts.check_create_settings(interaction.guild_id)

            db = database_manager.SQLiteManager()
            await db.connect()

            level_up_message_enabled = await db.execute_one("SELECT level_up_message_enabled FROM settings WHERE guild_id = ?", interaction.guild.id)
            level_up_message_enabled = level_up_message_enabled[0]
            if level_up_message_enabled:
                await db.execute("UPDATE settings SET level_up_message_enabled = 0")
                await interaction.response.send_message("Level up messages have been disabled.")
            else:
                await db.execute("UPDATE settings SET level_up_message_enabled = 1")
                await interaction.response.send_message("Level up messages have been enabled.")
            
            await db.commit()
            await db.disconnect()

        # level_up_message Command
        @self.tree.command(
            name="level_up_message",
            description="Set the level_up_message.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def level_up_message(interaction: discord.Interaction, message: str) -> None:
            await database_scripts.check_create_settings(interaction.guild_id)

            db = database_manager.SQLiteManager()
            await db.connect()
            await db.execute("UPDATE settings SET level_up_message = ? WHERE guild_id = ?", message, interaction.guild.id)
            await db.commit()
            await db.disconnect()

            await interaction.response.send_message(f"level_up_message has been set to `{message}`.")

        # level_up_message_channel_id Command
        @self.tree.command(
            name="level_up_message_channel_id",
            description="Set the level_up_message_channel_id.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def level_up_message_channel_id(interaction: discord.Interaction, channel_id: str) -> None:
            if not channel_id.isdigit():
                await interaction.response.send_message("Invalid channel ID. Please provide a valid integer ID.", ephemeral=True)
                return
            channel_id = int(channel_id)
            try:
                await self.client.fetch_channel(channel_id)
            except discord.errors.NotFound:
                await interaction.response.send_message("Channel not found. Please provide a valid channel ID.", ephemeral=True)
                return
            
            await database_scripts.check_create_settings(interaction.guild_id)

            db = database_manager.SQLiteManager()
            await db.connect()
            await db.execute("UPDATE settings SET level_up_message_channel_id = ? WHERE guild_id = ?", channel_id, interaction.guild.id)
            await db.commit()
            await db.disconnect()

            await interaction.response.send_message(f"level_up_message_channel_id has been set to `{channel_id}`.")

        """
        Slash Command Error Handling
        """

        # @self.tree.error
        # async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
        #     logger.log_error(error)
        #     await interaction.response.send_message(f"{error}", ephemeral=True)


    def run(self):
        self.client.run(self.env.get_token())
