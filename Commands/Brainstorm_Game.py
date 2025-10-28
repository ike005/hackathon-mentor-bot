import asyncio
import random
import discord
from discord.ext.commands import bot

from Button_Views.Brainstorming_Views.user_interest_option import SelectInterestOptions
from Button_Views.Brainstorming_Views.view_more_options import MoreOptionChoice



async def get_user_interests(interaction: discord.Interaction):
    await interaction.response.send_message("Please enter 2-4 of your interests (Separated in comma): ")


    def check(m: discord.Message):
        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

    try:

        msg = await bot.wait_for("message", check=check, timeout=60)
        choices = msg.content.split(",")

        if not 2 <= len(choices) <= 4:
            await interaction.followup.send("❌ Please enter between 2 to 4 interests.")
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


async def brainstormGame(interaction: discord.Interaction):

    organizer_interests = ["Time Travel", "Space Colonization", "Underwater Exploration"]

    user_interests = await get_user_interests(interaction)

    final_choice = await present_options(interaction, user_interests, organizer_interests)

    await interaction.channel.send(
        "Final remembered interests:\n" + "\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(final_choice))
    )