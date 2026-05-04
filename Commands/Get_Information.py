import datetime

import discord
from flask_app import mydb

class BasicIntroModal(discord.ui.Modal, title="Quick Intro"):
    name = discord.ui.Label(
        text='Name',
        component=discord.ui.TextInput(placeholder="Enter your name here")
    )

    age = discord.ui.Label(
        text='Age',
        component=discord.ui.TextInput(placeholder="Enter your age here")
    )

    gender = discord.ui.Label(
        text='Gender',
        component=discord.ui.TextInput(placeholder="Enter your gender here")
    )

    github_link = discord.ui.Label(
        text='Github Link',
        component=discord.ui.TextInput(placeholder="Enter your github link here")
    )

    email = discord.ui.Label(
        text='Email',
        component=discord.ui.TextInput(placeholder="Enter your email here")
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.component.value
        age = self.age.component.value
        gender = self.gender.component.value
        github_link = self.github_link.component.value
        email = self.email.component.value

        mycol = mydb["users_new"]

        user_data = {
            "user_id": str(interaction.user.id),
            "username": str(interaction.user),
            "name": name,
            "age": age,
            "gender": gender,
            "github_link": github_link,
            "email": email,
            # "created_at": datetime.utcnow()
        }

        mycol.update_one(
            {"user_id": str(interaction.user.id)},
            {"$set": user_data},
            upsert=True
        )

        # mycol.insert_one(user_data)

        message = f"""
        Thanks, {name}! 🎉
        Here’s a summary of your profile:
        • Name: {name}  
        • Age: {age}  
        • Gender: {gender}  
        • GitHub: {github_link}  
        • Email: {email}
            
        If anything looks off, feel free to update it anytime!
        """

        await interaction.response.send_message(message, ephemeral=True)


async def Intro_and_information(interaction: discord.Interaction):
    await interaction.response.send_modal(BasicIntroModal())