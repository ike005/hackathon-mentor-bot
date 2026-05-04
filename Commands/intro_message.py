import discord

from flask_app import mydb

intro_message = """
**Welcome to the server 👋**

We’re glad to have you here. This bot is here to help you check in, track how things are going, and use guided activities in the server.

**Commands**
`/start` — Begin using the bot and get set up
`/log` — Submit your daily check-in, feelings, and progress
`/brainstormgame` — Start the brainstorming activity for game ideas
`/help` — View all available commands

**How to get started**
Type `/start` and follow the prompts from the bot.

After that, you can:

* use `/log` for your daily check-in
* use `/brainstormgame` to build and explore ideas
* use `/help` anytime you need guidance

We’re excited to have you here. Get started with `/start` 🚀
"""

# class BasicIntroModal(discord.ui.Modal, title="Quick Intro"):
#     name = discord.ui.Label(text='Name', component=discord.ui.TextInput( placeholder="Enter your name here", required=True, max_length=100))
#     answer = discord.ui.Label(text='answer', component=discord.ui.TextInput( placeholder="Enter your answer here", required=True, max_length=100))
#
#
#     async def on_submit(self, interaction: discord.Interaction):
#         new_my_col = mydb["users_new"]
#
#         user_data = {
#             "user_id": str(interaction.user.id),
#             "username": str(interaction.user),
#             "name": {self.name.value}
#         }
#
#         new_my_col.insert_one(user_data)
#
#         await interaction.response.send_message(
#             f"Welcome {self.name.value}! answer is {self.answer.value}",
#             ephemeral=True
#         )

async def intro(interaction: discord.Interaction):
    # await interaction.response.send_modal(BasicIntroModal())
    await interaction.response.send_message(f"{intro_message}")
