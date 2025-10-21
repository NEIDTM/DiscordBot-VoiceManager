# DiscordBot-VoiceManager

A **Discord bot** built with [Disnake](https://docs.disnake.dev/) that allows users to create **voice channels** with full control over their settings. Perfect for communities that want private rooms with permissions and moderation features.

---

## Features

- Automatically create a **private voice channel** when a user joins a designated "creator" voice channel.
- Full **control panel** for the channel owner:
  - Set **user limit** (0 = unlimited)
  - Set **bitrate**
  - **Rename channel**
  - **Kick users**
  - **Block/unblock users**
  - **Toggle video**
  - **Grant/remove moderator permissions**
- Auto-delete empty private channels.
- Save settings in JSON files:
  - `server_settings.json` → target voice channels for each server
  - `channel_owners.json` → track owners and moderators

---

## Commands

### Administrator Commands

- `/setvoice <channel>` – Set a voice channel to automatically create private rooms.
- `/removevoice` – Remove the voice creator channel setting.

### Fun Command

- `/hello` – Sends a fun message to test the bot.

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/DiscordBot-VoiceManager.git
cd DiscordBot-VoiceManager
```

2. **Install dependencies:**

```bash
pip install disnake
```

3. **Create a bot on Discord Developer Portal** and get your token.

4. **Set your bot token** in the script:

```python
bot.run("YOUR_TOKEN_HERE")
```

5. **Run the bot:**

```bash
python bot.py
```

---

## Files

* `bot.py` – Main bot code.
* `server_settings.json` – Stores target voice channels per server.
* `channel_owners.json` – Stores owners and moderators for private channels.

---

## How It Works

1. A user joins the designated voice channel.
2. The bot creates a **new voice channel** with the user as the owner.
3. The owner gets a **control panel** with buttons to manage the channel.
4. The bot **automatically deletes** the channel when it's empty.

---
