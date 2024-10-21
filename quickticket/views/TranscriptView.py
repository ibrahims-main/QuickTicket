from helper.ticket_helper import generate_link
from discord.ui import Button, View
import discord

class TranscriptButton(View):
    def __init__(self, member, guild_id):
        super().__init__()

        self.member = member
        self.guild_id = guild_id

        # Generate link using the member and guild_id
        link = generate_link(self.member, self.guild_id)

        # Create the button to view the transcript
        self.add_item(Button(label="View Your Ticket", style=discord.ButtonStyle.link, url=link, emoji="🔗"))