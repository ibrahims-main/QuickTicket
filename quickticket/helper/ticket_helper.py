import sqlite3
import discord
from helper.githubFuncs import upload

def get_moderator_roles(guild_id: int) -> list[int]:
    try:
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT moderator_roles FROM ticketing_setup WHERE guild_id = ?", (guild_id,))
            result = cur.fetchone()

            if result:
                # Split the string of role IDs into a list of integers
                return list(map(int, result[0].split(',')))
            return []  # Return an empty list if no roles are found
    except sqlite3.Error as e:
        print(f"Error fetching moderator roles for guild {guild_id}: {e}")
        return []

def get_ticket_channel_id(guild_id: int) -> int:
    try:
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT ticket_channel_id FROM ticketing_setup WHERE guild_id = ?", (guild_id,))
            result = cur.fetchone()

            if result:
                return result[0]
            return None  # Return None if no ticket channel ID is found
    except sqlite3.Error as e:
        print(f"Error fetching ticket channel ID for guild {guild_id}: {e}")
        return None

def get_github_name_and_repo(guild_id: int) -> tuple[str, str]:
    try:
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT github_username, repository_name FROM ticketing_setup WHERE guild_id =?", (guild_id,))
            result = cur.fetchone()

            if result:
                return result[0], result[1]
            else:
                raise ValueError(f"No GitHub username and repository found for guild {guild_id}")
    except (sqlite3.Error, ValueError) as e:
        print(f"Error fetching GitHub name and repo for guild {guild_id}: {e}")
        raise

def generate_link(member: discord.Member, guild_id: int) -> str:
    try:
        file_name = upload(f"{member.id}.html", member.name, guild_id)
        github_username, repository_name = get_github_name_and_repo(guild_id)
        link = f"https://{github_username}.github.io/{repository_name}/tickets/{file_name}"
        return link
    except Exception as e:
        print(f"Error generating link for member {member.id} in guild {guild_id}: {e}")
        return ""