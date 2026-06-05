import discord


class MoreOptionChoice(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None  # Will be set to True for Yes or False for No

    # 'Yes' button handling
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def option_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()  # Conclude user interaction

    # 'No' button handling
    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def option_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()
