import discord
from discord.ui import Button, View, button
from helper.ticket_helper import *
from helper.log import send_log
from views.TicketCloseView import CloseButton

class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Create a Ticket", style=discord.ButtonStyle.blurple, custom_id="ticketopen", emoji="🎫")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.response.defer(ephemeral=True)

            # Fetch ticket category ID from database
            ticket_channel_id = get_ticket_channel_id(interaction.guild.id)
            category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=ticket_channel_id)

            # Check if category exists
            if category is None:
                await interaction.followup.send("Ticket category not found. Please contact an administrator.", ephemeral=True)
                return

            # Check if user already has an open ticket
            for ch in category.text_channels:
                if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                    await interaction.followup.send(f"You already have an open ticket in {ch.mention}.", ephemeral=True)
                    return

            # Fetch moderator roles from database
            moderator_roles_ids = get_moderator_roles(interaction.guild.id)

            # Create permission overwrites
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            }

            # Add permissions for each moderator role
            for role_id in moderator_roles_ids:
                role = interaction.guild.get_role(role_id)
                if role:  # Check if the role exists
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)

            # Add permissions for the user and the bot
            overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            overwrites[interaction.guild.me] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            # Create the text channel
            channel = await category.create_text_channel(
                name=str(interaction.user),
                topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
                overwrites=overwrites
            )

            # Send confirmation to ticket channel
            await channel.send(
                embed=discord.Embed(
                    title="Ticket Created!",
                    description="Don't ping the staff member, they will be here soon.",
                    color=discord.Color.random()
                ),
                view=CloseButton()
            )

            # Send confirmation to user
            await interaction.followup.send(
                embed=discord.Embed(
                    description=f"Created your ticket at {channel.mention}",
                    color=discord.Color.blurple()
                ),
                ephemeral=True
            )

            # Log ticket creation
            await send_log(
                title="Ticket Created",
                description=f"Created by {interaction.user.mention}",
                color=discord.Color.random(),
                guild=interaction.guild
            )

        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
            print(f"Error creating ticket: {e}")