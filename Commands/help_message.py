import discord
from datetime import datetime


def build_help_embed(user: discord.abc.User) -> discord.Embed:
    embed = discord.Embed(
        title="👋 Welcome to the Server!",
        description=(
            "We're excited to have you here. This bot helps you track daily progress, "
            "log feelings and productivity, brainstorm creative ideas, and build your personal profile."
        ),
        color=discord.Color.blurple(),
        timestamp=datetime.now(),
    )
    embed.set_author(
        name=user.display_name,
        icon_url=user.display_avatar.url,
    )
    embed.add_field(
        name="⚡ Slash Commands",
        value=(
            "`/profile` — Set up your personal profile and introduction\n"
            "`/log` — Submit your daily journal, motivation, and tasks\n"
            "`/brainstorm` — Start brainstorming for new game or project ideas\n"
            "`/help` — View this help guide anytime"
        ),
        inline=False,
    )
    embed.add_field(
        name="1️⃣ First Time Here?",
        value="Use `/profile` to add your name, age, gender, GitHub, and email.",
        inline=False,
    )
    embed.add_field(
        name="2️⃣ Daily Progress Tracking",
        value=(
            "Use `/log` to record how you're feeling, reflect on progress, "
            "prioritize tasks, and save your journal."
        ),
        inline=False,
    )
    embed.add_field(
        name="3️⃣ Brainstorming Mode",
        value=(
            "Use `/brainstorm` for creative game ideas, team planning, "
            "and innovation sessions."
        ),
        inline=False,
    )
    embed.add_field(
        name="4️⃣ Need Assistance?",
        value="Use `/help` anytime you need command guidance.",
        inline=False,
    )
    embed.add_field(
        name="🌟 Recommended Flow",
        value="`/profile` → `/log` → `/brainstorm`",
        inline=False,
    )
    embed.set_footer(
        text="We're glad you're here — let's build something amazing together! 🚀"
    )
    return embed


async def Help_Message(interaction: discord.Interaction):
    embed = build_help_embed(interaction.user)
    await interaction.followup.send(embed=embed, ephemeral=True)
