import sqlite3
import discord
from discord.ext import commands
from asyncio import TimeoutError
from views.TicketOpenView import CreateButton

async def setup_ticketing(ctx, bot: commands.Bot):
    def check_channel(m):
        return m.author == ctx.author and m.channel_mentions

    def check_roles(m):
        return m.author == ctx.author and all(role in m.role_mentions for role in m.role_mentions)

    def check_yes_no(m):
        return m.author == ctx.author and m.content.lower() in ["yes", "no"]

    guild_id = ctx.guild.id  # Get the guild ID of the server where the command is used

    try:
        # Ask for ticketing channel
        await ctx.send("Please mention the ticketing channel.")
        ticketing_msg = await bot.wait_for("message", check=check_channel, timeout=60)
        ticket_channel = ticketing_msg.channel_mentions[0]
        ticket_channel_id = ticket_channel.id

        # Ask if logging is needed
        await ctx.send("Do you want to enable logging? (yes/no)")
        log_choice_msg = await bot.wait_for("message", check=check_yes_no, timeout=60)
        log_choice = log_choice_msg.content.lower()

        log_channel_id = None  # Initialize log_channel_id

        if log_choice == "yes":
            # Ask for log channel
            await ctx.send("Please mention the log channel.")
            log_msg = await bot.wait_for("message", check=check_channel, timeout=60)
            log_channel = log_msg.channel_mentions[0]
            log_channel_id = log_channel.id

        # Ask for moderator roles
        await ctx.send("Please mention all the moderator roles who can moderate the tickets.")
        roles_msg = await bot.wait_for("message", check=check_roles, timeout=60)
        moderator_roles = [role.id for role in roles_msg.role_mentions]
        moderator_roles_str = ",".join(map(str, moderator_roles))  # Convert to string for storing in SQLite

        # Ask for GitHub username
        await ctx.send("Please enter your GitHub username.")
        github_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
        github_username = github_msg.content

        # Ask for GitHub repository name
        await ctx.send("Please enter your GitHub repository name.")
        repo_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
        repository_name = repo_msg.content

        # Ask for GitHub token
        await ctx.send("Please enter your GitHub token.")
        token_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
        github_token = token_msg.content.strip()  # Store the token securely

        # Insert the data into the database using guild_id as the primary key
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()

            # Optional: Delete previous setup if it exists for this guild
            cur.execute("DELETE FROM ticketing_setup WHERE guild_id = ?", (guild_id,))

            # Insert the new setup (log_channel_id could be NULL if logging is not enabled)
            cur.execute(""" 
                INSERT INTO ticketing_setup (guild_id, ticket_channel_id, log_channel_id, moderator_roles, github_username, repository_name, github_token)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (guild_id, ticket_channel_id, log_channel_id, moderator_roles_str, github_username, repository_name, github_token))

            conn.commit()

            channel: discord.TextChannel = await bot.get_channel(ticket_channel_id)

            embed = discord.Embed(
                title="Open a New Ticket",
                description="Open a new ticket for asking questions (just dont troll)",
                color=discord.Color.green()
            )

            await channel.send(embed=embed, view=CreateButton())

        await ctx.send("Ticketing setup completed successfully!")

    except discord.errors.NotFound:
        await ctx.send("The mentioned channel or role could not be found.")
    except discord.errors.Forbidden:
        await ctx.send("I don't have permission to perform that action.")
    except discord.errors.HTTPException as http_error:
        await ctx.send(f"HTTP error occurred: {http_error}")
    except TimeoutError:
        await ctx.send("You took too long to respond.")
    except Exception as e:
        await ctx.send(f"An error occurred during setup: {e}")