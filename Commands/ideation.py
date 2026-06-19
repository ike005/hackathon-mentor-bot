import asyncio
import random
import discord
from datetime import datetime


from Button_Views.Ideation_Views.user_interest_option import SelectInterestOptions
from Button_Views.Ideation_Views.view_more_options import MoreOptionChoice
from flask_app import mydb


async def get_user_interests(interaction: discord.Interaction):
    await interaction.followup.send(f"Please enter 2 - 4 of your interests(Separated in comma):")

    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    while True:
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            choices = [choice.strip() for choice in msg.content.split(",") if choice.strip()]

            if not 2 <= len(choices) <= 4:
                await interaction.followup.send("❌ Please enter between 2 to 4 interests.")
                continue
            return choices
        except asyncio.TimeoutError:
            await interaction.followup.send("⌛ You didn’t respond in time.")
            return []


async def get_user_reason_for_interests(interaction: discord.Interaction):
    await interaction.followup.send(f"Why did you choose these interests, and what makes them personally meaningful to you:")

    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:
        msg = await interaction.client.wait_for("message", check=check, timeout=60)

        return msg.content
    except asyncio.TimeoutError:
        await interaction.followup.send("⌛ You didn’t respond in time.")
        return []

async def get_user_possible_project_impact(interaction: discord.Interaction):
    await interaction.followup.send(
        f"Which industry, community, or audience does this project aim to impact? Please provide a comma-separated list (e.g., Education, Students, Local Communities, Healthcare, Small Businesses)\n ")

    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    while True:
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            choices = [choice.strip() for choice in msg.content.split(",") if choice.strip()]

            if not choices:
                await interaction.followup.send("❌ Please enter at least 1 industry, community, or audience.")
                return
            return choices
        except asyncio.TimeoutError:
            await interaction.followup.send("⌛ You didn’t respond in time.")
            return []


async def get_user_techstack_interests(interaction: discord.Interaction):
    await interaction.followup.send(f"Which technologies do you plan to use for this project? \n Please list them separated by commas (e.g., JavaScript, Python, Flask, React, MongoDB).:")

    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    while True:
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            choices = [choice.strip() for choice in msg.content.split(",") if choice.strip()]

            if not choices:
                await interaction.followup.send("❌ Please enter at least 1 Tech stack.")
                return
            return choices
        except asyncio.TimeoutError:
            await interaction.followup.send("⌛ You didn’t respond in time.")
            return []


async def get_user_possible_tools_utilized(interaction: discord.Interaction):
    await interaction.followup.send(
        f"While working on this project, which resources or tools do you expect to use when you encounter a roadblock? \n Please enter a comma-separated list (e.g., YouTube, Stack Overflow, AI tools, documentation, Discord communities, GitHub, online tutorials).")

    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    while True:
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)
            choices = [choice.strip() for choice in msg.content.split(",") if choice.strip()]

            if not choices:
                await interaction.followup.send("❌ Please enter at least 1 resources or tools you might use.")
                return
            return choices
        except asyncio.TimeoutError:
            await interaction.followup.send("⌛ You didn’t respond in time.")
            return []

async def present_options(interaction: discord.Interaction, user_interests, organizer_interests):
    remembered = []
    while True:
        # Get interests that have not yet been picked in any prior round
        available_organizer_option = [i for i in organizer_interests if i not in remembered]
        available_user_option = [i for i in user_interests if i not in remembered]


        number_of_random_user = 2
        if len(available_user_option) < 2:
            number_of_random_user = 1
            if len(available_user_option) < 1:

                await interaction.followup.send(
                    "Not enough new interests from your input, moving to the organizers."
                )
                number_of_random_user = 0


        number_of_random_organizer = 2
        if len(available_organizer_option) < 2:
            number_of_random_organizer = 1
            if len(available_organizer_option) < 1:

                await interaction.followup.send("Not enough new interests to continue.")
                break

        if number_of_random_organizer > 0:
            organizer_random_interest = random.sample(available_organizer_option, number_of_random_organizer)
        else:
            organizer_random_interest = []

        if number_of_random_user > 0:
            user_random_interest = random.sample(available_user_option, number_of_random_user)
        else:
            user_random_interest = []


        option_interests = organizer_random_interest + user_random_interest


        if not option_interests:
            await interaction.channel.send("No more new interests to select from. Ending session.")
            break


        options_text = ""
        for index, option in enumerate(option_interests):
            options_text += f"{index + 1}. {option}\n"


        view_so = SelectInterestOptions()
        await interaction.followup.send(f"Select 2-3 options that interest you \n{options_text}", view=view_so)
        await view_so.wait()

        # If the user clicked Exit in the view, stop the loop gracefully
        if getattr(view_so, "exited", False):
            await interaction.channel.send("ℹ️ Selection flow exited by user. Ending brainstorming options.")
            break

        selected = view_so.selected_values

        if not (2 <= len(selected) <= 3):
            await interaction.channel.send("❌ You must select between 2 and 3 options.")
            continue


        selected_options = []
        for i in selected:
            if 0 <= i - 1 < len(option_interests):
                selected_options.append(option_interests[i - 1])
            else:
                await interaction.channel.send("❌ Invalid option selected.")
                return


        remembered.extend(selected_options)
        await interaction.channel.send("You selected:\n" + "\n".join(f"- {opt}" for opt in selected_options))


        view_yn = MoreOptionChoice()
        await interaction.followup.send("🔁 Do you want to view more options? (yes/no)", view=view_yn)
        await view_yn.wait()

        if view_yn.value is False:
            break

    return remembered


async def Ideation(interaction: discord.Interaction):

    organizer_interests = ["Time Travel", "Space Colonization", "Underwater Exploration"]

    user_interests = await get_user_interests(interaction)

    final_choice = await present_options(interaction, user_interests, organizer_interests)
    user_reason_for_interest = await get_user_reason_for_interests(interaction)
    user_possible_project_impact = await get_user_possible_project_impact(interaction)
    user_techstack = await get_user_techstack_interests(interaction)
    user_tools_utilized = await get_user_possible_tools_utilized(interaction)

    today = datetime.now().strftime("%Y-%m-%d")

    mycol = mydb["brainstorming"]

    mycol.update_one(
        {
            "user_id": interaction.user.id,
        },
        {
            "$set": {
                f"user_interests": final_choice,
                f"log_date": today,
            }
        },
        upsert=True
    )

    embed = discord.Embed(
        title="🎯 Brainstorming Session Summary",
        description=f"**Date:** {today}",
        color=discord.Color.blurple(),
        timestamp=datetime.now(),
    )
    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url,
    )
    embed.add_field(name="🔍 Selected Interests", value="\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(final_choice)), inline=False)
    embed.add_field(name="💭 Why These Interests?", value=user_reason_for_interest, inline=False)
    embed.add_field(name="🎯 Intended Project Impact", value="\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(user_possible_project_impact)), inline=False)
    embed.add_field(name="Tech Stack", value="\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(user_techstack)), inline=False)
    embed.add_field(name="🛠 Resources & Tools", value="\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(user_tools_utilized.strip(""))),inline=False)

    embed.set_footer(
        text="Your brainstorming session has been saved. You can view it anytime."
    )

    await interaction.channel.send(embed=embed)