"""
Confessy Bot - Anonymous Confession Discord Bot (Multi-Server Edition)

This bot allows users to submit anonymous confessions to a Discord channel.
Each server can configure its own confession and logs channels.

Author: Najdz3l
Version: 1.0.0
License: MIT
"""

import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - retrieve from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot configuration with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Configuration file
CONFIG_FILE = 'server_config.json'


def load_config():
    """Load server configuration from JSON file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save server configuration to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_guild_config(guild_id: int):
    """Get configuration for a specific guild"""
    config = load_config()
    return config.get(str(guild_id), {})


def set_guild_config(guild_id: int, confession_channel_id: int, logs_channel_id: int):
    """Set configuration for a specific guild"""
    config = load_config()
    config[str(guild_id)] = {
        'confession_channel_id': confession_channel_id,
        'logs_channel_id': logs_channel_id
    }
    save_config(config)


@bot.event
async def on_ready():
    """
    Event triggered when bot successfully connects to Discord.
    Syncs application commands and prints connection status.
    """
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    print("Application commands synchronized!")


@bot.tree.command(name="setup", description="Configure confession and logs channels")
@discord.app_commands.describe(
    confession_channel="Channel for confessions",
    logs_channel="Channel for moderation logs"
)
async def setup(
    interaction: discord.Interaction,
    confession_channel: discord.TextChannel,
    logs_channel: discord.TextChannel
):
    """
    Setup command to configure channels for this server.
    Only server administrators can use this.

    Args:
        interaction: Discord interaction object
        confession_channel: The channel where confessions will be posted
        logs_channel: The channel where logs will be stored
    """
    # Check if user has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Only administrators can use this command!",
            ephemeral=True
        )
        return

    # Verify bot permissions
    if not confession_channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message(
            f"I don't have permission to send messages in {confession_channel.mention}",
            ephemeral=True
        )
        return

    if not logs_channel.permissions_for(interaction.guild.me).send_messages:
        await interaction.response.send_message(
            f"I don't have permission to send messages in {logs_channel.mention}",
            ephemeral=True
        )
        return

    # Save configuration
    set_guild_config(
        interaction.guild.id,
        confession_channel.id,
        logs_channel.id
    )

    # Send confirmation
    await interaction.response.send_message(
        f"Configuration saved!\n"
        f"Confessions: {confession_channel.mention}\n"
        f"Logs: {logs_channel.mention}",
        ephemeral=True
    )


@bot.tree.command(name="confession", description="Submit an anonymous confession")
@discord.app_commands.describe(text="Your confession text")
async def confession(interaction: discord.Interaction, text: str):
    """
    Slash command to submit an anonymous confession.

    Args:
        interaction (discord.Interaction): Discord interaction object
        text (str): The confession text (max 2000 characters)

    Behavior:
        - Posts the confession anonymously to the configured confession channel
        - Logs the submission (with user info) to the configured logs channel
        - Sends a confirmation message (ephemeral) to the user
    """
    # Get guild configuration
    guild_config = get_guild_config(interaction.guild.id)

    # Check if server is configured
    if not guild_config or 'confession_channel_id' not in guild_config:
        await interaction.response.send_message(
            "This server hasn't been configured yet!\n"
            "Please ask an administrator to use `/setup` command.",
            ephemeral=True
        )
        return

    # Get the target channels
    confession_channel = interaction.client.get_channel(
        guild_config['confession_channel_id']
    )
    logs_channel = interaction.client.get_channel(
        guild_config['logs_channel_id']
    )

    # Verify channels exist
    if not confession_channel or not logs_channel:
        await interaction.response.send_message(
            "Configured channels no longer exist!\n"
            "Please ask an administrator to run `/setup` again.",
            ephemeral=True
        )
        return

    # Create and send the anonymous confession embed
    embed = discord.Embed(
        title="Anonymous Confession",
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
