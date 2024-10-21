# quickticket/quickticket.py

from helper.database import create_tables  # Import for setting up the database
from helper.setup_helper import setup_ticketing  # Import for setting up the ticketing system
from discord.ext import commands

class QuickTicket:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @classmethod
    async def setup(self, bot: commands.Bot):
        # Create database tables when setting up
        await create_tables()

        # Call the setup function for ticketing
        await setup_ticketing(bot)

        # Log that the ticket system was set up successfully
        print("Ticketing system setup complete!")

        # Return the instance of QuickTicket
        return self(bot)