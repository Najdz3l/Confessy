# Confessy Bot

An anonymous confession Discord bot that allows users to submit confessions to a dedicated channel while maintaining anonymity. Each server can configure its own confession and moderation channels. All submissions are logged for oversight and security.

## Features

- Anonymous Submissions - Users can confess without revealing their identity to other users
- Multi-Server Support - Use the same bot on unlimited Discord servers with separate configurations
- Per-Server Setup - Each server configures its own confession and logs channels
- Rich Formatting - Confessions are displayed in beautiful embeds
- Logging & Moderation - All submissions are logged with timestamps and user information
- Slash Commands - Modern Discord slash command integration
- Easy Configuration - Simple `/setup` command for administrators

## Requirements

- Python 3.8+
- discord.py 2.0+
- python-dotenv

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Najdz3l/Confessy.git
cd Confessy
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux (Bash/Zsh)
python -m venv venv
source venv/bin/activate

# On macOS/Linux (Fish shell)
python -m venv venv
source venv/bin/activate.fish
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your token:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DISCORD_TOKEN=your_bot_token_here
```

### 5. Run the Bot

```bash
python main.py
```

You should see:

```
Logged in as BotName#1234
Application commands synchronized!
```

## Usage

### Server Setup (Administrators Only)

First, an administrator must configure the bot for their server:

```
/setup #confessions-channel #logs-channel
```

This tells the bot which channels to use for:

- **confessions-channel**: Where anonymous confessions are posted
- **logs-channel**: Where moderation logs are stored (private to moderators)

### Submitting a Confession

Users can then submit confessions using:

```
/confession Your confession text here
```

The bot will:

1. Post your confession anonymously to the configured confession channel
2. Log the submission details (with your user info) to the logs channel (for moderation only)
3. Send you a confirmation message (visible only to you)

## Configuration

### Environment Variables

| Variable        | Description            | Example                              |
| --------------- | ---------------------- | ------------------------------------ |
| `DISCORD_TOKEN` | Your Discord bot token | `MTk4NjIyNDgzMjM4MjQwOTI4.C5XeEQ...` |

### Per-Server Configuration

Server configurations are stored in `server_config.json`. This file is automatically created when an administrator runs `/setup` for the first time on a server.

Example `server_config.json`:

```json
{
  "123456789": {
    "confession_channel_id": 987654321,
    "logs_channel_id": 111222333
  },
  "444555666": {
    "confession_channel_id": 777888999,
    "logs_channel_id": 222333444
  }
}
```

Each guild (server) ID maps to its own confession and logs channels.

### Getting Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application
3. Go to the "Bot" tab
4. Click "Add Bot"
5. Under "TOKEN", click "Copy"
6. Paste it in your `.env` file as `DISCORD_TOKEN=...`

### Adding Bot to Your Server

1. In [Discord Developer Portal](https://discord.com/developers/applications)
2. Go to OAuth2 > URL Generator
3. Select scopes: `bot`
4. Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
5. Copy the generated URL and open it in your browser
6. Select your server and authorize

## Project Structure

```
Confessy/
├── main.py              # Main bot file
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Environment variables (git-ignored)
├── .gitignore           # Git ignore rules
├── server_config.json   # Per-server configurations (auto-created)
├── LICENSE              # MIT License
└── README.md            # This file
```

## Hosting on Wispbyte

### Pre-Startup Script

Use this in Wispbyte's "Startup" (or "Pre-startup script") field:

```bash
if [ -d Confessy/.git ]; then (cd Confessy && git pull); else git clone --depth 1 https://github.com/Najdz3l/Confessy.git; fi && cp -r Confessy/* . 2>/dev/null; rm -rf Confessy 2>/dev/null; if [[ ! -f .env ]]; then echo "DISCORD_TOKEN=" > .env; fi; if [[ -f requirements.txt ]]; then pip install -U --prefix .local -r requirements.txt; fi && python main.py
```

### Configuration on Wispbyte

1. **Project URL**: `https://github.com/Najdz3l/Confessy.git`
2. **Auto Update**: Set `AUTO_UPDATE` to `1` to automatically pull changes
3. **Main File**: `main.py`
4. **Additional Packages**: Leave empty (installer from requirements.txt)
5. **Environment Variables**:
   - `DISCORD_TOKEN`: Your Discord bot token

### After First Startup

Once the bot starts on Wispbyte:

1. Go to **Files** section
2. Edit `.env` file
3. Add your `DISCORD_TOKEN`
4. Restart the server

## Logging

All confessions are logged to the configured logs channel with:

- Timestamp
- Username who submitted it
- User ID
- Full confession text

This allows server moderators to identify and act on inappropriate content if needed.

## Security & Privacy

- Confessions are posted anonymously to regular users
- `.env` file is git-ignored to prevent token exposure
- `server_config.json` is git-ignored to protect channel configurations
- Logs are stored in a private channel for moderation only
- Never commit `.env` file to version control

## Troubleshooting

### Bot not responding to /setup or /confession

The server hasn't been configured yet. Make sure:

1. An administrator ran `/setup #confessions-channel #logs-channel`
2. Both channels exist and the bot has permission to access them
3. Restart the bot

### "I don't have permission to send messages in [channel]"

The bot role doesn't have the required permissions. Fix:

1. Go to Server Settings > Roles
2. Find the bot role
3. Give it: "Send Messages", "Embed Links", "Read Message History"
4. Try `/setup` again

### "Only administrators can use this command!"

Only Discord server administrators can run `/setup`. Regular users can only use `/confession`.

### Bot showing "This server hasn't been configured yet!"

The `/setup` command hasn't been run on this server. Ask an administrator to run:

```
/setup #confessions-channel #logs-channel
```

### "This command is outdated, please try again in a few minutes"

The bot's command cache is outdated. Solution:

- Restart the bot (Ctrl+C, then run `python main.py` again)
- Wait a minute and try the command again

### "Improper token has been passed"

- Check your `.env` file has the correct `DISCORD_TOKEN`
- Make sure you're using the bot token, not the client ID
- The token should start with your bot's ID

### Bot doesn't show logs in the logs channel

Make sure the bot has permission to send messages in the logs channel. Check:

1. Channel permissions for the bot role
2. The channel exists and bot can access it
3. Run `/setup` again to reconfigure if needed

### No module named 'discord' on Wispbyte

The dependencies are not installed. The pre-startup script should handle it, but manually restart the server if needed. Check logs for installation errors.

## Contributing

Feel free to fork this project and submit pull requests!

## License

MIT License - see LICENSE file for details

## Support

If you encounter any issues, please open an issue on GitHub.

## Disclaimer

This bot is provided as-is. Server administrators are responsible for moderating the content posted through this bot. Users should follow Discord's Terms of Service and your server's rules.
