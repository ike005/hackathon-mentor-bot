import discord


class SelectInterestOptions(discord.ui.View):
    def __init__(self):
        # Initialize the selection view with a 60-second timeout
        super().__init__(timeout=60)
        self.selected_values = []  # Store values (option numbers) user has picked

    # Handles what happens when a selection button is clicked
    async def handle_selection(self, interaction: discord.Interaction, value: int, button: discord.ui.Button):
        if value not in self.selected_values:  # Prevent duplicate selections
            self.selected_values.append(value)  # Record this selection
            button.disabled = True             # Disable the clicked button
            await interaction.response.edit_message(view=self)  # Reflect the button's new state

    # Button for selecting option 1
    @discord.ui.button(label='1', style=discord.ButtonStyle.success)
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 1, button)

    # Button for selecting option 2
    @discord.ui.button(label='2', style=discord.ButtonStyle.success)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 2, button)

    # Button for selecting option 3
    @discord.ui.button(label='3', style=discord.ButtonStyle.success)
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 3, button)

    # Button for selecting option 4
    @discord.ui.button(label='4', style=discord.ButtonStyle.success)
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, 4, button)

    # 'Done' button to complete the selection
    @discord.ui.button(label='Done', style=discord.ButtonStyle.danger)
    async def option_done(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the correct number of options were selected
        if not (2 <= len(self.selected_values) <= 3):
            await interaction.response.send_message(
                "❌ Please select between 2 and 3 options before finishing.",
                ephemeral=True
            )
            return  # Exit if the requirement is not met
        # Disable all buttons after user finishes selection
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)  # Update button states for the user
        await interaction.followup.send("🎉 Selection complete!", ephemeral=True)  # Confirm selection to the user
        self.stop()  # End the view and unblock the waiting coroutine