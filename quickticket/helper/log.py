import discord
import sqlite3
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Connect to the SQLite database
conn = sqlite3.connect("helper/database.db")
cur = conn.cursor()

async def send_log(guild: discord.Guild, title: str, description: str, color: discord.Color, view: discord.ui.View = None):
    try:
        # Fetch the log channel ID associated with the guild and user
        cur.execute("SELECT log_channel_id FROM ticketing_setup WHERE guild_id = ?", (guild.id,))
        result = cur.fetchone()

        if result is None or result[0] is None:
            logging.warning(f"No log channel found for guild {guild.name} (ID: {guild.id})")
            return  # Exit if no log channel is found for this guild
        
        log_channel_id = result[0]
        channel = guild.get_channel(log_channel_id)
        
        if channel is None:
            logging.warning(f"Channel ID {log_channel_id} not found in guild {guild.name}")
            return  # Exit if the channel does not exist in the guild

        # Create the embed for the log message
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        # Send the embed to the specified log channel with optional view
        await channel.send(embed=embed, view=view)

        logging.info(f"Sent log message to {channel.name} in guild {guild.name}")

    except sqlite3.Error as db_error:
        logging.error(f"Database error while sending log: {db_error}")
    except discord.HTTPException as discord_error:
        logging.error(f"Discord API error while sending log: {discord_error}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while sending log: {e}")