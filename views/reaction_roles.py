import discord


class ReactionRoles(discord.ui.View):
    def __init__(self, label: str, style: discord.ButtonStyle, role: discord.Role) -> None:
        super().__init__(timeout=None)
        self.label = label
        self.style = style
        self.role = role

        button = discord.ui.Button(label=self.label, custom_id=self.label, style=self.style) # TODO custom_id should be unique
        button.callback = self.button_callback
        self.add_item(button)


    async def button_callback(self, interaction: discord.Interaction):
        member = interaction.user
        role = self.role

        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Role {role.name} removed!", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Role {role.name} added!", ephemeral=True)
