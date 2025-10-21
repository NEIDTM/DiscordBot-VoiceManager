# 🎙️ DiscordBot-VoiceManager

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="50" height="50"/>
  <img src="https://ru.guide.disnake.dev/public/disnake-logo.png" alt="Disnake" width="50" height="50"/>
  <img src="https://cdn.brandfetch.io/idM8Hlme1a/theme/dark/symbol.svg?c=1dxbfHSJFAPEGdCLU4o5B" alt="Discord" width="50" height="50"/>
</p>

**A Discord bot built with [Disnake](https://docs.disnake.dev/) that allows users to create temporary voice channels with full control over settings and permissions.**

<div align="center">

[Features](#-features) • [Requirements](#-requirements) • [Installation](#-installation) • [Usage](#-usage) • [Commands](#️-commands)

</div>

---

## ✨ Features

- 🎯 **Automatic Channel Creation** – Create a voice channel when joining a designated "creator" channel
- 🎛️ **Full Control Panel** – Interactive button-based control system
- 👥 **User Limit Management** – Set custom user limits (0-99, 0 = unlimited)
- 🎵 **Bitrate Control** – Adjust audio quality (8-96 kbps)
- ✏️ **Channel Renaming** – Customize your channel name
- 👢 **Kick System** – Remove users from your channel
- 🚫 **Block/Unblock Users** – Prevent specific users from joining
- 📹 **Video Toggle** – Enable or disable video streaming
- 🔑 **Moderator System** – Grant control permissions to other users
- 🗑️ **Auto-Cleanup** – Channels are automatically deleted when empty
- 💾 **Persistent Settings** – Server and channel settings saved in JSON files

---

## 🛠 Requirements

Before installation, make sure you have:

- **Python 3.8+**
- **pip** (Python package manager)
- **Discord Bot Token** (from Discord Developer Portal)

### Installing Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT:** Check **"Add Python to PATH"** during installation
4. Verify installation:
```bash
python --version
```

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 📦 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/NEIDTM/DiscordBot-VoiceManager.git
cd DiscordBot-VoiceManager
```

### Step 2: Install Dependencies
```bash
pip install disnake
```

If you encounter permission errors on Linux/macOS:
```bash
pip install --user disnake
```

### Step 3: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Go to the **"Bot"** section in the left sidebar
4. Click **"Add Bot"** and confirm
5. Under the bot's username, click **"Reset Token"** and copy the token
6. **Enable these Privileged Gateway Intents:**
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent (optional)

### Step 4: Invite the Bot to Your Server

1. In the Developer Portal, go to **"OAuth2"** → **"URL Generator"**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Manage Channels
   - ✅ Move Members
   - ✅ View Channels
   - ✅ Send Messages
   - ✅ Connect
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### Step 5: Configure the Bot

1. Open the `bot.py` file in any text editor
2. Find this line at the bottom of the file:
   ```python
   bot.run("YOUR_TOKEN_HERE")
   ```
3. Replace `YOUR_TOKEN_HERE` with your actual bot token:
   ```python
   bot.run("MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GaBcDe.FgHiJkLmNoPqRsTuVwXyZ1234567890")
   ```
4. Save the file

### Step 6: Run the Bot

```bash
python bot.py
```

If you see `Bot is ready! Logged in as YourBotName#1234`, your bot is running! 🎉

**Keep the terminal window open** - the bot will stop if you close it.

---

## 🚀 Usage

### Setting Up the Voice Creator Channel

1. **Create a voice channel** in your Discord server (or use an existing one)
2. Use the command in Discord:
   ```
   /setvoice channel:#your-voice-channel
   ```
3. The bot will confirm the setup with a ✅ message

### Creating Your Own Voice Channel

1. **Join the designated creator channel**
2. You'll be **automatically moved** to a new voice channel
3. The channel will be named `YourName's Voice`
4. A **control panel** will appear in the text chat of your channel

### Using the Control Panel

The control panel has interactive buttons for:

| Button | Function | Who Can Use |
|--------|----------|-------------|
| 👥 **Set User Limit** | Set max users (0-99, 0 = unlimited) | Owner & Moderators |
| 🎵 **Set Bitrate** | Adjust audio quality (8-96 kbps) | Owner & Moderators |
| ✏️ **Rename Channel** | Change channel name | Owner & Moderators |
| 👢 **Kick User** | Remove a user from the channel | Owner & Moderators |
| 🚫 **Block User** | Prevent a user from joining | Owner & Moderators |
| ✅ **Unblock User** | Allow blocked user to join | Owner & Moderators |
| 📹 **Toggle Video** | Enable/disable video streaming | Owner & Moderators |
| 🔑 **Give Permissions** | Grant moderator access | Owner only |
| 🔓 **Remove Permissions** | Revoke moderator access | Owner only |

### Example Workflow

```
1. User joins "🎤 Create Voice" channel
   ↓
2. Bot creates "John's Voice" and moves user there
   ↓
3. Control panel appears with all buttons
   ↓
4. John clicks "👥 Set User Limit" → enters "5"
   ↓
5. John clicks "🔑 Give Permissions" → selects "Sarah"
   ↓
6. Sarah can now use all control buttons
   ↓
7. When everyone leaves, the channel is automatically deleted
```

---

## 🛠️ Commands

### Administrator Commands

**`/setvoice <channel>`**
- Sets a voice channel as the "creator" channel
- Requires: Administrator permission
- Example: `/setvoice channel:#create-voice`

**`/removevoice`**
- Removes the voice creator channel setting
- Requires: Administrator permission

### Fun Command

**`/hello`**
- Sends a test message to verify the bot is working
- Available to everyone

---

## 📂 Project Structure

```
DiscordBot-VoiceManager/
├── bot.py                      # Main bot code
├── server_settings.json        # Stores target voice channels per server (auto-created)
└── channel_owners.json         # Tracks channel owners and moderators (auto-created)
```

**Note:** JSON files are created automatically when the bot runs for the first time.

---

## ⚙️ How It Works

1. **User joins creator channel** → Bot detects the voice state change
2. **Permission setup** → Bot creates overwrites for the owner
3. **Channel creation** → New voice channel is created in the same category
4. **User moved** → User is automatically moved to the new channel
5. **Owner assigned** → User becomes the channel owner with full permissions
6. **Control panel sent** → Interactive embed with buttons appears
7. **Settings saved** → Owner and moderator data stored in JSON
8. **Auto-deletion** → Bot monitors the channel and deletes it when empty

---

## 🔧 Advanced Configuration

### Running in Background (Linux/macOS)

To keep the bot running after closing the terminal:

```bash
nohup python bot.py &
```

To stop the bot:
```bash
pkill -f bot.py
```

### Running as a Service (Linux)

Create a systemd service file `/etc/systemd/system/discordbot.service`:

```ini
[Unit]
Description=Discord Voice Manager Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/DiscordBot-VoiceManager
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable discordbot
sudo systemctl start discordbot
sudo systemctl status discordbot
```

### Running on Windows Startup

1. Create a batch file `start_bot.bat`:
```batch
@echo off
cd C:\path\to\DiscordBot-VoiceManager
python bot.py
pause
```

2. Press `Win + R` → type `shell:startup` → press Enter
3. Place the batch file in the opened folder

---

<div align="center">

**Made with ❤️ for Discord communities**

⭐ Star this project if you like it!

</div>
