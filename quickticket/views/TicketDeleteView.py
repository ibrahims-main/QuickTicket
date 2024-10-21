import discord
import asyncio
from discord.ui import View, button, Button
from helper.log import send_log

class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Delete Ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.response.defer()
            await interaction.channel.send("Deleting the ticket in 3 seconds...")
            await asyncio.sleep(3)
            await interaction.channel.delete()

            # Log ticket deletion
            await send_log(
                title="Ticket Deleted",
                description=f"Deleted by {interaction.user.mention}, ticket: {interaction.channel.name}",
                color=discord.Color.red(),
                guild=interaction.guild
            )

        except discord.Forbidden:
            await interaction.channel.send("I don't have permission to delete this ticket channel.")
        except discord.HTTPException as e:
            await interaction.channel.send(f"Failed to delete the ticket channel: {e}")
        except Exception as e:
            await interaction.channel.send(f"An error occurred during ticket deletion: {e}")
            print(f"Error deleting ticket: {e}")