import asyncio
import random
import discord
from datetime import datetime

from Button_Views.Daily_Log_View.motivation_level import MotivationLevel
from Button_Views.Daily_Log_View.task_selection import TaskSelection
from flask_app import mydb



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

        taskIndexes = view_ts.selected_tasks
        tasks = []
        for i in taskIndexes:
            tasks.append(combinedTask[i - 1])

        if len(tasks) != 2:
            await interaction.followup.send(f"You selected: {len(tasks)} tasks. Please select 2 tasks.")
            continue
        else:
            break

    return tasks

class JournalTextModal(discord.ui.Modal, title="Daily Reflection"):

    def __init__(self):
        super().__init__()
        self.user_response = None

    reflection = discord.ui.TextInput(
        label="How are things going today?",
        style=discord.TextStyle.paragraph,
        placeholder="Explain in detail how things are going for you or your team...",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.user_response = self.reflection.value

        await interaction.response.send_message("✅ Your reflection has been recorded!",ephemeral=True)


async def get_user_text_feeling(interaction: discord.Interaction):
    modal = JournalTextModal()
    await interaction.response.send_modal(modal)

    await modal.wait()

    return modal.user_response



async def Daily_Log(interaction: discord.Interaction):
    try:

        user_text_feeling = await get_user_text_feeling(interaction)

        user_display_name = interaction.user.display_name
        await interaction.followup.send(
            f"Hi there {user_display_name}! 👋",
            ephemeral=True
        )

        user_feeling = await get_user_motivation_level(interaction)
        # await interaction.followup.send("You selected:"+ "\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(user_feeling)))
        #
        # await interaction.followup.send(f"📝 Reflection saved:\n{user_text_feeling}",ephemeral=True)

        user_tasks = await get_user_task_selection(interaction)
        # await interaction.followup.send("You selected:" + "\n".join(f"{opt}" for opt in user_tasks))

        mycol = mydb["daily_log"]

        today = datetime.now().strftime("%Y-%m-%d")

        mycol.update_one(
            {
                "user_id": interaction.user.id,
            },
            {
                "$set": {
                    f"log_date": today,
                    f"user_feeling": user_feeling,
                    f"user_text_feeling": user_text_feeling,
                    f"user_tasks": user_tasks,
                }
            },
            upsert=True
        )

        # summary_message = f"""
        #     Here’s a summary of your log:
        #     • Feeling: {user_text_feeling}
        #     • Emotion: {user_feeling}
        #     • Tasks: {user_tasks}
        #     {today}
        #
        #     If anything looks off, feel free to update it anytime!
        # """

        motivation = user_feeling[0] if user_feeling else "Not specified"
        task_list = "\n".join(f"• {task}" for task in user_tasks)

        if "Stressed" in motivation:
            embed_color = discord.Color.red()
        elif "Okay" in motivation:
            embed_color = discord.Color.gold()
        elif "Good" in motivation:
            embed_color = discord.Color.green()
        else:
            embed_color = discord.Color.from_rgb(87, 242, 135)

        embed = discord.Embed(
            title="📓 Daily Log Summary",
            description=f"**Date:** {today}",
            color=embed_color,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name=user_display_name,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.add_field(
            name="💭 Reflection",
            value=user_text_feeling or "—",
            inline=False,
        )
        embed.add_field(
            name="🎯 Motivation Level",
            value=motivation,
            inline=True,
        )
        embed.add_field(
            name="✅ Priority Tasks",
            value=task_list or "—",
            inline=False,
        )
        embed.set_footer(
            text="Your daily log has been saved. You can update it anytime if your priorities change."
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    except asyncio.TimeoutError:
        await interaction.channel.send("⌛ You didn’t respond in time.")
    except Exception as e:
        await interaction.channel.send(f"Something went wrong: {e}")