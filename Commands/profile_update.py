import discord
from datetime import datetime

from Mongodb_integrations.insert_data_to_mongodb import insert_data_into_profile_collection

class BasicIntroModal(discord.ui.Modal, title="Quick Intro"):
    name = discord.ui.TextInput(
        label="Name",
        placeholder="Enter your name here"
    )

    age = discord.ui.TextInput(
        label="Age",
        placeholder="Enter your age here"
    )

    gender = discord.ui.TextInput(
        label="Gender",
        placeholder="Enter your gender here"
    )

    github_link = discord.ui.TextInput(
        label="Github Link",
        placeholder="Enter your github link here"
    )

    email = discord.ui.TextInput(
        label="Email",
        placeholder="Enter your email here"
    )

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        age = self.age.value
        gender = self.gender.value
        github_link = self.github_link.value
        email = self.email.value

        data = {
            "username": str(interaction.user),
            "name": name,
            "age": age,
            "gender": gender,
            "github_link": github_link,
            "email": email,
        }

        insert_data_into_profile_collection(interaction.user.id, data)

        github_display = (
            f"[GitHub Profile]({github_link})"
            if github_link.startswith(("http://", "https://"))
            else github_link or "—"
        )

        embed = discord.Embed(
            title="👤 Profile Summary",
            description=f"Thanks, **{name}**! 🎉",
            color=discord.Color.blurple(),
            timestamp=datetime.now(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.add_field(name="📛 Name", value=name or "—", inline=True)
        embed.add_field(name="🎂 Age", value=age or "—", inline=True)
        embed.add_field(name="⚧ Gender", value=gender or "—", inline=True)
        embed.add_field(name="🔗 GitHub", value=github_display, inline=False)
        embed.add_field(name="📧 Email", value=email or "—", inline=False)
        embed.set_footer(
            text="Your profile has been saved. You can update it anytime if anything looks off."
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def Profile_Update(interaction: discord.Interaction):
    await interaction.response.send_modal(BasicIntroModal())