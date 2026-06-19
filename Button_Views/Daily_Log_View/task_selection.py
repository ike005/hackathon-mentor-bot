import discord


class TaskSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.selected_tasks = []

    async def handle_selection(self, interaction: discord.Interaction, value: int, button: discord.ui.Button):
        if value not in self.selected_tasks:  # Prevent duplicate selections
            self.selected_tasks.append(value)  # Record this selection
            button.disabled = True  # Disable the clicked button
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label='1', style=discord.ButtonStyle.success)
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 1, button)
        if len(self.selected_tasks) == 2:
            self.stop()

    # Button for selecting option 2
    @discord.ui.button(label='2', style=discord.ButtonStyle.success)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 2, button)
        if len(self.selected_tasks) == 2:
            self.stop()

    # Button for selecting option 3
    @discord.ui.button(label='3', style=discord.ButtonStyle.success)
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 3, button)
        if len(self.selected_tasks) == 2:
            self.stop()

    # Button for selecting option 4
    @discord.ui.button(label='4', style=discord.ButtonStyle.success)
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 4, button)
        if len(self.selected_tasks) == 2:
            self.stop()