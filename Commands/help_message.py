import discord

intro_message = """
# 👋 Welcome to the Server!

We’re excited to have you here. This bot is designed to help you:
- Track daily progress
- Log feelings and productivity
- Brainstorm creative ideas
- Build your personal profile

##  Available Slash Commands

`/profile` — Set up your personal profile and introduction information  
`/log` — Submit your daily journal, motivation, and task progress  
`/brainstorm` — Start the brainstorming activity for new game or project ideas  
`/help` — View this help guide anytime  

##  Getting Started

### 1️⃣ First Time Here?
Use:
`/profile`

This will help you:
- Add your name
- Age
- Gender
- GitHub
- Email

---

### 2️⃣ Daily Progress Tracking
Use:
`/log`

This allows you to:
- Record how you're feeling
- Reflect on daily/team progress
- Prioritize tasks
- Save your journal

---

### 3️⃣ Brainstorming Mode
Use:
`/brainstorm`

Perfect for:
- Creative game ideas
- Team planning
- Innovation sessions

---

### 4️⃣ Need Assistance?
Use:
`/help`

Anytime you need command guidance.

---

## 🌟 Recommended Flow
`/profile` → `/log` → `/brainstorm`

We’re glad you’re here — let’s build something amazing together! 🚀
"""

async def Help_Message(interaction: discord.Interaction):
    await interaction.followup.send(intro_message, ephemeral=True)