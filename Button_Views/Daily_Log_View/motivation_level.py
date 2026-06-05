import discord

class MotivationLevel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.selected_MotivationLevel = []

    async def handle_selection(self, interaction: discord.Interaction, value: str, button: discord.ui.Button):
        if value not in self.selected_MotivationLevel:  # Prevent duplicate selections
            self.selected_MotivationLevel.append(value)  # Record this selection
            button.disabled = True  # Disable the clicked button
            await interaction.response.edit_message(view=self)  # Reflect the button's new state


    @discord.ui.button(label='Super excited',emoji="😁", style=discord.ButtonStyle.success)
    async def Level1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "Super excited 😁", button)
        self.stop()

    @discord.ui.button(label='Good',emoji="😊", style=discord.ButtonStyle.success)
    async def Level2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "Good 😊", button)
        self.stop()

    @discord.ui.button(label='Okay',emoji="😐" , style=discord.ButtonStyle.success)
    async def Level3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "Okay 😐", button)
        self.stop()

    @discord.ui.button(label='Stressed', emoji="😞" , style=discord.ButtonStyle.success)
    async def Level4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "Stressed 😞", button)
        self.stop()