# Hackathon Mentor Bot

A Discord bot that helps hackathon attendees track progress, log daily reflections, brainstorm ideas, and build profiles. Organizers can also schedule DMs to users or roles.

## Prerequisites

Before you start, make sure you have:

- **Python 3.10+** (3.11 or 3.12 recommended)
- A **Discord account** with permission to create or manage a bot
- A **Discord server** (guild) where you can test the bot
- A **MongoDB Atlas** cluster (or other MongoDB instance) for storing user data

## Project structure

```
hackathon-mentor-bot/
├── main.py              # Bot entry point — run this to start the bot
├── flask_app.py         # MongoDB connection (used by slash commands)
├── Commands/            # Slash command handlers (/log, /brainstorm, etc.)
├── Button_Views/        # Discord button/modal UI components
├── file_count.py        # Optional script to pull GitHub repo stats into MongoDB
├── requirements.txt     # Python dependencies
└── .env                 # Local secrets (you create this — not in git)
```

## 1. Clone and install dependencies

```bash
git clone https://github.com/<your-org>/hackathon-mentor-bot.git
cd hackathon-mentor-bot

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Optional (Conda):** If you prefer Conda, you can use `requirement_conda.yaml` instead, then install any remaining packages from `requirements.txt`.

**Plotly charts:** The `$my_temps` command saves a chart image. If that command fails with an image export error, install Kaleido:

```bash
pip install kaleido
```

## 2. Create a Discord bot

Follow the [discord.py introduction guide](https://discordpy.readthedocs.io/en/stable/discord.html) to:

1. Create an application in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Add a **Bot** user and copy the **Bot Token**.
3. Under **Privileged Gateway Intents**, enable:
   - **Message Content Intent**
   - **Server Members Intent**
4. Invite the bot to your test server with permissions to:
   - Send messages
   - Use slash commands
   - Read message history

### Get your Discord IDs

Turn on **Developer Mode** in Discord (User Settings → Advanced → Developer Mode), then:

| Value | How to get it |
|-------|----------------|
| `DISCORD_GUILD` | Right-click your server name → **Copy Server ID** |
| `HACKATHON_CHANNEL_ID` | Right-click the channel where slash commands should work → **Copy Channel ID** |

## 3. Set up MongoDB

1. Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a database user with read/write access.
3. Allow your IP address in **Network Access** (or `0.0.0.0/0` for local testing only).
4. Copy the username and password for your `.env` file.

The bot uses the database name `hackathonbot` with collections such as `users_new`, `daily_log`, and `brainstorming`.

## 4. Configure environment variables

Create a `.env` file in the project root (this file is gitignored):

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD=your_discord_server_id
HACKATHON_CHANNEL_ID=your_hackathon_channel_id

MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
```

**Optional** (only needed for `file_count.py`):

```env
GITHUB_PAT=your_github_personal_access_token
```

## 5. Run the bot

```bash
python main.py
```

If setup is correct, you should see output similar to:

```
Logged in as YourBotName#1234
Synced 4 command(s).
```

The bot writes logs to `discord.log` in the project root.

To stop the bot, press `Ctrl+C` in the terminal.

## 6. Test the application

There is no automated test suite in this repo yet, so testing is done manually in Discord.

### Quick smoke test

1. Start the bot (`python main.py`).
2. In your Discord server, confirm the bot appears online.
3. In the channel matching `HACKATHON_CHANNEL_ID`, run `/help`.
4. Confirm the bot responds with the help message.

> **Note:** Most slash commands (`/log`, `/brainstorm`, `/help`) only work in the channel whose ID matches `HACKATHON_CHANNEL_ID`. `/profile` works in any channel.

### Slash commands (recommended user flow)

Run these in order in your hackathon channel:

| Command | What to test | Expected result |
|---------|--------------|-----------------|
| `/profile` | Fill out the modal (name, age, gender, GitHub, email) | Bot confirms your profile; data saved to MongoDB `users_new` |
| `/log` | Submit reflection text, pick motivation level, choose 2 tasks | Bot confirms journal saved; data saved to MongoDB `daily_log` |
| `/brainstorm` | Enter 2–4 comma-separated interests, select options via buttons | Bot walks through interest selection and saves to MongoDB `brainstorming` |
| `/help` | Run anytime | Bot sends the help guide |

### Prefix commands (admin / legacy)

These use the `$` prefix in any channel where the bot can read messages:

| Command | Who can use it | What to test |
|---------|----------------|--------------|
| `$hello` | Anyone | Bot replies `Hello!` |
| `$99` | Anyone | Bot sends a random Brooklyn 99 quote |
| `$my_temps` | Anyone | Shows thermometer check-in history (if you have responses) |
| `$schedule` | Server administrators | Interactive flow to schedule one-time or recurring DMs |
| `$schedule-list` | Server administrators | Lists scheduled jobs |
| `$schedule-remove <job_id>` | Server administrators | Removes a scheduled job |

### Thermometer check-in

Posting in a specific update channel triggers a DM survey (Function, Elegance, Effort, Resources on a 1–10 scale). Responses are saved under `thermometer_responses/`. Use `$my_temps` to view your history and chart.

> The update channel ID is currently hardcoded in `main.py`. For local testing, you may need to change that ID to match your test channel, or test in the configured channel.

### Verify data in MongoDB

After running `/profile`, `/log`, or `/brainstorm`, open MongoDB Atlas and confirm documents appear in:

- `hackathonbot.users_new`
- `hackathonbot.daily_log`
- `hackathonbot.brainstorming`

### Optional: GitHub stats script

`file_count.py` fetches GitHub repository statistics and inserts them into MongoDB. It is separate from the Discord bot and requires additional configuration:

```bash
python file_count.py
```

You may need to update the repository list and MongoDB connection settings inside that script before running it.

## Troubleshooting

| Problem | Likely fix |
|---------|------------|
| Bot does not come online | Check `DISCORD_TOKEN` in `.env` |
| Slash commands do not appear | Confirm `DISCORD_GUILD` matches your server ID; restart the bot |
| "This command can only be used in #channel" | Run the command in the channel matching `HACKATHON_CHANNEL_ID` |
| MongoDB connection errors | Verify `MONGO_USERNAME` / `MONGO_PASSWORD` and Atlas network access |
| `$my_temps` image export fails | Run `pip install kaleido` |
| Bot cannot DM users | User must allow DMs from server members |

## Features overview

**Organizers can:**
- Schedule DMs to attendees by username or role (one-time or recurring)
- List and remove scheduled jobs

**Hackers can:**
- Set up a profile with `/profile`
- Log daily progress and motivation with `/log`
- Brainstorm project ideas with `/brainstorm`
- Complete thermometer check-ins via DM
- View personal thermometer trends with `$my_temps`

The thermometer check-in is inspired by John Hunter's work in *World Peace And Other 4th-Grade Achievements* (Harper Collins, 2014).

## User flow

[User Flow Diagram (tldraw)](https://www.tldraw.com/s/v2_c_mIoelW-FkU6DonizF8qRQ?d=v230.-740.3166.1844.u3uTLtOXOF0gz0ZSLETkT)

## License

See the repository for license details.
