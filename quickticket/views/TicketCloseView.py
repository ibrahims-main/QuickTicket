import discord
import sqlite3
from asyncio import sleep
from discord.ui import View, Button, button
from helper.ticket_helper import get_moderator_roles, get_ticket_channel_id
from helper.log import send_log
from helper.githubFuncs import get_transcript
from views.TranscriptView import TranscriptButton
from views.TicketDeleteView import TrashButton

# Establish SQLite connection
conn = sqlite3.connect("helper/database.db")
cur = conn.cursor()

class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="closeticket")
    async def close(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.response.defer(ephemeral=True)

            await interaction.channel.send("Closing the ticket in 3 seconds!...")
            await sleep(3)

            # Fetch the moderator roles from the database
            moderator_roles_ids = get_moderator_roles(interaction.guild.id)

            # Create the permission overwrites
            ticket_channel_id = get_ticket_channel_id(interaction.guild.id)
            category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=ticket_channel_id)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            }

            # Add permissions for each moderator role from the database
            for role_id in moderator_roles_ids:
                role = interaction.guild.get_role(role_id)
                if role:  # Check if the role exists
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)

            # Add permissions for the user and the bot
            overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            overwrites[interaction.guild.me] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            # Edit the channel's overwrites
            await interaction.channel.edit(category=category, overwrites=overwrites)
            await interaction.channel.send(
                embed=discord.Embed(
                    description="Ticket Closed!",
                    color=discord.Color.red()
                ),
                view=TrashButton()
            )

            # Get member and generate transcript
            member = interaction.guild.get_member(int(interaction.channel.topic.split(" ")[0]))
            await get_transcript(member=member, channel=interaction.channel)

            # Send log message
            await send_log(
                title="Ticket Closed",
                description=f"Closed by: {interaction.user.mention}",
                color=discord.Color.yellow(),
                guild=interaction.guild,
                view=TranscriptButton(member, interaction.guild.id)
            )

        except Exception as e:
            await interaction.channel.send(f"An error occurred during ticket closure: {e}")
            print(f"Error closing ticket: {e}")