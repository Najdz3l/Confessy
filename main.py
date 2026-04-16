"""
Confessy Bot - Anonymous Confession Discord Bot

This bot allows users to submit anonymous confessions to a Discord channel.
All confessions are logged for moderation purposes.

Author: Your Name
Version: 1.0.0
License: MIT
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - retrieve from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CONFESSION_CHANNEL_ID = int(os.getenv('CONFESSION_CHANNEL_ID'))
LOGS_CHANNEL_ID = int(os.getenv('LOGS_CHANNEL_ID'))

# Bot configuration with required intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    """
    Event triggered when bot successfully connects to Discord.
    Syncs application commands and prints connection status.
    """
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    print("Application commands synchronized!")


@bot.tree.command(name="confession", description="Submit an anonymous confession")
async def confession(interaction: discord.Interaction, text: str):
    """
    Slash command to submit an anonymous confession.

    Args:
        interaction (discord.Interaction): Discord interaction object
        text (str): The confession text (max 2000 characters)

    Behavior:
        - Posts the confession anonymously to the confession channel
        - Logs the submission (with user info) to the logs channel
        - Sends a confirmation message (ephemeral) to the user
    """
    # Get the target channels
    confession_channel = interaction.client.get_channel(CONFESSION_CHANNEL_ID)
    logs_channel = interaction.client.get_channel(LOGS_CHANNEL_ID)

    # Create and send the anonymous confession embed
    embed = discord.Embed(
        title="📝 Anonymous Confession",
        description=text,
        color=discord.Color.purple()
    )
    await confession_channel.send(embed=embed)

    # Log the confession with user information for moderation
    timestamp = discord.utils.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"""
    ```markdown
Timestamp: {timestamp}
User: {interaction.user}
User ID: {interaction.user.id}
Content: {text}
```"""
    await logs_channel.send(log_message)

    # Send confirmation to user (only they can see it - ephemeral)
    await interaction.response.send_message(
        "Your confession has been submitted anonymously!",
        ephemeral=True
    )


# Start the bot
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
