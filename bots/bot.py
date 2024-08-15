import discord

from data.env import Env
from events import guild_remove_event, message_delete_event, raw_reaction_add_event, ready_event, message_event, guild_join_event
from commands import help_command, leaderboard_command, level_command, ping_command, button_role_command, reaction_role_command, settings_command
from utils import logger


class Bot:
    def __init__(self, env: Env) -> None:
        self.env = env
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.client = discord.Client(intents=self.intents)
        self.tree = discord.app_commands.CommandTree(self.client)

        self.ready = False

        """
        Events
        """

        @self.client.event
        async def on_ready() -> None:
            # await self.tree.sync(guild=discord.Object(id=self.env.get_test_guild_id()))
            # await self.tree.sync()

            await ready_event.on_ready(self.client)
            print("Logged on as", self.client.user)
            self.ready = True

        
        @self.client.event
        async def on_message(message: discord.Message) -> None:
            if not self.ready:
                return
            
            await message_event.on_message(self.client, message)
        

        @self.client.event
        async def on_message_delete(message: discord.Message) -> None:
            if not self.ready:
                return
            
            await message_delete_event.on_message_delete(self.client, message)
        

        @self.client.event
        async def on_guild_join(guild: discord.Guild) -> None:
            if not self.ready:
                return
            
            await guild_join_event.on_guild_join(self.client, guild)
        

        @self.client.event
        async def on_guild_remove(guild: discord.Guild) -> None:
            if not self.ready:
                return
            
            await guild_remove_event.on_guild_remove(self.client, guild)
        

        @self.client.event
        @discord.app_commands.checks.bot_has_permissions(manage_roles=True)
        async def on_raw_reaction_add(raw_reaction: discord.RawReactionActionEvent) -> None:
            if not self.ready:
                return
            
            await raw_reaction_add_event.on_raw_reaction_add(self.client, raw_reaction)
        
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
            discord.app_commands.Choice(name="level", value="level"),
            discord.app_commands.Choice(name="leaderboard", value="leaderboard"),
        ])
        async def help(interaction: discord.Interaction, command: discord.app_commands.Choice[str] = None) -> None:
            if not self.ready:
                return
            
            command_value = command.value if command else None
            await help_command.on_help(self.client, interaction, command_value)
        

        # Ping Command
        @self.tree.command(
            name="ping",
            description="Displays the bots reponse time und latency.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.bot_has_permissions(send_messages=True)
        async def ping(interaction: discord.Interaction) -> None:
            if not self.ready:
                return
            
            await ping_command.on_ping(self.client, interaction)
        

        # Button Role Command
        @self.tree.command(
            name="button_role",
            description="Creates a button that assigns a role to the user.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.bot_has_permissions(send_messages=True, manage_roles=True)
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def button_role(interaction: discord.Interaction, message_text: str, label: str, role: discord.Role) -> None:
            if not self.ready:
                return
            
            await button_role_command.on_button_role(self.client, interaction, message_text, label, role)
        

        # Settings Command
        @self.tree.command(
            name="settings",
            description="Display and manage the server's settings.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.choices(setting=[
            discord.app_commands.Choice(name="leveling_enabled", value="leveling_enabled"),
            discord.app_commands.Choice(name="xp_gain_cooldown_secs", value="xp_gain_cooldown_secs"),
            discord.app_commands.Choice(name="xp_per_message", value="xp_per_message"),
            discord.app_commands.Choice(name="level_up_message_enabled", value="level_up_message_enabled"),
            discord.app_commands.Choice(name="level_up_message", value="level_up_message"),
            discord.app_commands.Choice(name="level_up_message_channel_id", value="level_up_message_channel_id"),
        ])
        async def settings(interaction: discord.Interaction, setting: discord.app_commands.Choice[str] = None, new_value: str = None) -> None:
            if not self.ready:
                return
            
            setting_value = setting.value if setting else None
            await settings_command.on_settings(self.client, interaction, setting_value, new_value)
        

        # Level Command
        @self.tree.command(
            name="level",
            description="Displays your or another user's level.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        async def level(interaction: discord.Interaction, member: discord.Member = None) -> None:
            if not self.ready:
                return
            
            await level_command.on_level(self.client, interaction, member)
        

        # Leaderboard Command
        @self.tree.command(
            name="leaderboard",
            description="Displays the leaderboard of the users with the most levels.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        async def leaderboard(interaction: discord.Interaction) -> None:
            if not self.ready:
                return
            
            await leaderboard_command.on_leaderboard(self.client, interaction)
        

        # Reaction Role Command
        @self.tree.command(
            name="reaction_role",
            description="Creates a button that assigns a role to the user.",
            guild=discord.Object(id=self.env.get_test_guild_id())
        )
        @discord.app_commands.checks.bot_has_permissions(send_messages=True, manage_roles=True)
        @discord.app_commands.checks.has_permissions(administrator=True)
        async def reaction_role(
            interaction: discord.Interaction,
            message_text: str,
            emoji: str,
            role: discord.Role
        ) -> None:
            if not self.ready:
                return
            
            await reaction_role_command.on_reaction_role(self.client, interaction, message_text, emoji, role)

        """
        Slash Command Error Handling
        """

        @self.tree.error
        async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
            # Common Errors like missing permissions etc. that are allowed to happen and are handled here
            if isinstance(error, discord.app_commands.CommandOnCooldown):
                await interaction.response.send_message(f"Command is on cooldown. Please try again in {error.retry_after:.2f} seconds.", ephemeral=True)
                return
            if isinstance(error, discord.app_commands.BotMissingPermissions):
                missing_perms_str = ", ".join(error.missing_permissions)
                await interaction.response.send_message(f"Bot is missing the following permissions:\n{missing_perms_str}", ephemeral=True)
                return
            if isinstance(error, discord.app_commands.MissingPermissions):
                missing_perms_str = ", ".join(error.missing_permissions)
                await interaction.response.send_message(f"You are missing the following permissions:\n{missing_perms_str}", ephemeral=True)
                return
            
            # CommandInvokeError (Should not happen)
            if isinstance(error, discord.app_commands.CommandInvokeError):
                error_msg = f"Catched CommandInvokeError\n"
                error_msg += f"Command: {interaction.data.get("name")}\n"
                error_msg += f"Args: {interaction.data.get("options")}\n"
                error_msg += f"User: {interaction.user}\n"
                error_msg += f"Error: {error}"

                print(error_msg)
                l = logger.Logger()
                l.log_error(error_msg)
                print("Error has been logged to file.")

                await interaction.response.send_message(f"An internal error occured.", ephemeral=True)
                return
            
            # Unknown Error
            error_msg = f"An unknown error ({error.__class__}) has been catched while executing a command.\n"
            error_msg += f"Command: {interaction.data.get("name")}\n"
            error_msg += f"Args: {interaction.data.get("options")}\n"
            error_msg += f"User: {interaction.user}\n"
            error_msg += f"Error: {error}"

            print(error_msg)
            l = logger.Logger()
            l.log_error(error_msg)
            print("Error has been logged to file.")

            await interaction.response.send_message(f"An internal error occured.", ephemeral=True)


    def run(self):
        self.client.run(self.env.get_token())
