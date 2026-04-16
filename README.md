# Confessy Bot

An anonymous confession Discord bot that allows users to submit confessions to a dedicated channel while maintaining anonymity. All submissions are logged to a moderation channel for oversight and security.

## Features

- 🔐 **Anonymous Submissions** - Users can confess without revealing their identity to other users
- 📝 **Rich Formatting** - Confessions are displayed in beautiful embeds
- 📊 **Logging & Moderation** - All submissions are logged with timestamps and user information to a dedicated moderation channel
- ⚡ **Slash Commands** - Modern Discord slash command integration
- 🎨 **Attractive UI** - Purple themed embeds for visual appeal

## Requirements

- Python 3.8+
- discord.py 2.0+
- python-dotenv

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Confessy.git
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

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DISCORD_TOKEN=your_bot_token_here
CONFESSION_CHANNEL_ID=123456789
LOGS_CHANNEL_ID=987654321
```

### 5. Run the Bot

```bash
python bot.py
```

You should see:

```
Logged in as BotName#1234
Application commands synchronized!
```

## Usage

### Submitting a Confession

In Discord, simply use the slash command:

```
/confession Your confession text here
```

The bot will:

1. Post your confession anonymously to the confession channel
2. Log the submission details to the logs channel (for moderation)
3. Send you a confirmation message (visible only to you)

## Configuration

### Environment Variables

| Variable                | Description                                       | Example                              |
| ----------------------- | ------------------------------------------------- | ------------------------------------ |
| `DISCORD_TOKEN`         | Your Discord bot token                            | `MTk4NjIyNDgzMjM4MjQwOTI4.C5XeEQ...` |
| `CONFESSION_CHANNEL_ID` | Channel ID where confessions are posted           | `1234567890`                         |
| `LOGS_CHANNEL_ID`       | Channel ID where logs are stored (for moderation) | `0987654321`                         |

### Getting Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application
3. Go to the "Bot" tab
4. Click "Add Bot"
5. Under "TOKEN", click "Copy"
6. Paste it in your `.env` file

### Getting Channel IDs

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on a channel
3. Select "Copy Channel ID"
4. Paste it in your `.env` file

## Project Structure

```
Confessy/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Environment variables (git-ignored)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Logging

All confessions are logged to the logs channel with:

- Timestamp
- Username who submitted it
- User ID
- Full confession text

This allows server moderators to identify and act on inappropriate content if needed.

## Security & Privacy

- ✅ Confessions are posted anonymously to regular users
- ✅ `.env` file is git-ignored to prevent token exposure
- ✅ Logs are stored in a private channel for moderation only
- ⚠️ **Never commit `.env` file to version control**

## Troubleshooting

### "This environment is externally managed" (Arch Linux / CachyOS)

On Arch-based distributions, you must use a virtual environment:

```bash
# Make sure you created and activated venv first
python -m venv venv
source venv/bin/activate.fish  # For Fish shell
# or
source venv/bin/activate       # For Bash/Zsh

# Then install dependencies
pip install -r requirements.txt
```

### "This command is outdated, please try again in a few minutes"

The bot's command cache is outdated. Solution:

- Restart the bot (Ctrl+C, then run `python bot.py` again)
- Wait a minute and try the command again

### "Improper token has been passed"

- Check your `.env` file has the correct `DISCORD_TOKEN`
- Make sure you're using the bot token, not the client ID

### Bot doesn't respond

1. Make sure the bot has permissions to:
   - View the confession channel
   - Send messages in the confession channel
   - View and send messages in the logs channel

2. Check if the bot is running (`✅ Logged in as...` message shown)

### "No module named 'discord'" when running bot

The dependencies are not installed. Make sure:
1. Virtual environment is activated
2. Run: `pip install -r requirements.txt`
3. Then: `python bot.py`

## Contributing

Feel free to fork this project and submit pull requests!

## License

MIT License - see LICENSE file for details

## Support

If you encounter any issues, please open an issue on GitHub.

## Disclaimer

This bot is provided as-is. Server administrators are responsible for moderating the content posted through this bot. Users should follow Discord's Terms of Service and your server's rules.
