import discord


class ButtonRoles(discord.ui.View):
    def __init__(self, label: str, custom_id: str, style: discord.ButtonStyle, role: discord.Role) -> None:
        super().__init__(timeout=None)
        self.label = label
        self.custom_id = custom_id
        self.style = style
        self.role = role

        button = discord.ui.Button(label=self.label, custom_id=self.custom_id, style=self.style)
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
