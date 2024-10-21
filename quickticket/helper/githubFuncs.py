import discord
import chat_exporter
import time
import sqlite3
from github import Github
from os import remove, path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Function to get transcript of the ticket
async def get_transcript(member: discord.Member, channel: discord.TextChannel):
    export = await chat_exporter.export(channel=channel)
    if export is None:
        logging.error(f"Failed to export chat for channel {channel.name}")
        return None

    file_name = f"{member.id}.html"
    
    # Write the export to an HTML file
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(export)
        logging.info(f"Transcript for {channel.name} saved as {file_name}.")
    except Exception as e:
        logging.error(f"Error writing transcript for {channel.name}: {e}")
        return None

    return file_name

# Function to upload transcript to GitHub
def upload(file_path: str, member_name: str, guild_id: int):
    try:
        # Check if the file exists
        if not path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            return None

        # Fetch GitHub credentials from the database
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT github_token, github_username, repository_name FROM ticketing_setup WHERE guild_id = ?", (guild_id,))
            result = cur.fetchone()

        if result is None:
            logging.error(f"GitHub credentials not found for guild_id {guild_id}.")
            return None

        github_token, github_username, repository_name = result

        # Initialize GitHub instance
        github = Github(github_token)
        repo = github.get_repo(f"{github_username}/{repository_name}")

        # Generate a file name based on the current timestamp
        file_name = f"{int(time.time())}"

        # Read the file content before uploading
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Create the file in the repository
        repo.create_file(
            path=f"tickets/{file_name}.html",  # Path in the GitHub repository
            message=f"Ticket Log for {member_name}",
            branch="main",
            content=content
        )

        logging.info(f"Uploaded {file_path} as {file_name}.html to GitHub repository {repository_name}.")

        return file_name

    except sqlite3.Error as db_error:
        logging.error(f"Database error: {db_error}")
    except Exception as e:
        logging.error(f"An error occurred during the GitHub upload process: {e}")
        return None
    finally:
        # Clean up: Remove the local file after uploading
        if path.exists(file_path):
            try:
                remove(file_path)
                logging.info(f"Removed local file {file_path}.")
            except Exception as file_error:
                logging.error(f"Error removing local file {file_path}: {file_error}")