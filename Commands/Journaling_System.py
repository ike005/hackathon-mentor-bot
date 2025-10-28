import asyncio
import random
import discord

from Button_Views.Journaling_System_Views.motivation_level import MotivationLevel
from Button_Views.Journaling_System_Views.task_selection import TaskSelection



async def get_user_motivation_level(interaction: discord.Interaction):
    view_feel = MotivationLevel()
    await interaction.followup.send("How do you feel today? ", view=view_feel)
    await view_feel.wait()
    return view_feel.selected_MotivationLevel

async def get_user_task_selection(interaction: discord.Interaction):
    preTask = ["Fix mobile layout", "Finalize team roles"]
    comTask = ["Work on backend authentication", "Work on frontend authentication", "Set up database",
               "Craft new features"]

    randPre = random.sample(preTask, 2)
    randCom = random.sample(comTask, 2)

    combinedTask = randPre + randCom

    task_options = ""
    for index, option in enumerate(combinedTask):
        task_options += f"{index + 1}. {option}\n"

    while True:

        view_ts = TaskSelection()
        await interaction.followup.send(f"Select 2 tasks that you prioritize the most: \n{task_options}", view=view_ts)
        await view_ts.wait()

        tasks = view_ts.selected_tasks

        if len(tasks) != 2:
            await interaction.followup.send(f"You selected: {len(tasks)} tasks. Please select 2 tasks.")
            continue
        else:
            break

    return tasks




async def journalingSystem(interaction: discord.Interaction):
    user_display_name = interaction.user.display_name

    await interaction.response.send_message(f"Hi there {user_display_name}")

    try:
        user_feeling = await get_user_motivation_level(interaction)
        await interaction.followup.send("You selected:"+ "\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(user_feeling)))


        user_tasks = await get_user_task_selection(interaction)
        await interaction.followup.send("You selected:" + "\n".join(f"{opt}" for opt in user_tasks))

    except asyncio.TimeoutError:
        # Handle situation where user did not respond in time
        await interaction.channel.send("⌛ You didn’t respond in time.")
    except Exception as e:
        # General error handling
        await interaction.channel.send(f"Something went wrong: {e}")