# DiscordBot-VoiceManager 🎙️

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="50" height="50"/>
<img src="https://cdn.brandfetch.io/idM8Hlme1a/theme/dark/symbol.svg?c=1dxbfHSJFAPEGdCLU4o5B" alt="Discord" width="50" height="50"/>

A **Discord bot** built with [Disnake](https://docs.disnake.dev/) that allows users to create **voice channels** with full control over settings. Ideal for communities that want  rooms with permissions and moderation features.

---

## 🚀 Features

- Automatically create a **voice channel** when a user joins a designated "creator" voice channel.
- Full **control panel** for the channel owner:
  - 👥 Set **user limit** (0 = unlimited)
  - 🎵 Set **bitrate**
  - ✏️ **Rename channel**
  - 👢 **Kick users**
  - 🚫 **Block/unblock users**
  - 📹 **Toggle video**
  - 🔑 **Grant/remove moderator permissions**
- Auto-delete empty channels.
- Persist settings in JSON files:
  - `server_settings.json` → target voice channels per server
  - `channel_owners.json` → track owners and moderators

---

## 🛠️ Commands

### Administrator Commands
- `/setvoice <channel>` – Set a voice channel to automatically create rooms.
- `/removevoice` – Remove the voice creator channel setting.

### Fun Command
- `/hello` – Sends a test message to check the bot.

---

## ⚙️ Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/DiscordBot-VoiceManager.git
cd DiscordBot-VoiceManager
````

2. **Install dependencies:**

```bash
pip install disnake
```

3. **Create a Discord bot** via [Discord Developer Portal](https://discord.com/developers/applications) and get your token.

4. **Set your bot token** in `bot.py`:

```python
bot.run("YOUR_TOKEN_HERE")
```

5. **Run the bot:**

```bash
python bot.py
```

---

## 📁 Files

* `bot.py` – Main bot code.
* `server_settings.json` – Stores target voice channels per server.
* `channel_owners.json` – Stores owners and moderators for voice channels.

---

## 📝 How It Works

1. A user joins the designated "creator" voice channel.
2. The bot creates a **new voice channel** with the user as the owner.
3. The owner receives a **control panel** with buttons to manage the channel.
4. The bot **automatically deletes** the channel when it's empty.
