# QuickTicket

---

## Overview

QuickTicket is a powerful yet easy-to-use ticketing system library designed specifically for Discord bots. With QuickTicket, you can effortlessly create and manage support tickets, allowing your users to get assistance when they need it most. Our library is tailored for developers who want to implement a ticketing system without the hassle of complex configurations.

### Key Features

- *Simple Integration:* QuickTicket is designed to be integrated into your existing Discord bot with minimal effort.
- *User-Friendly:* Create a seamless experience for users to generate and manage tickets directly through Discord.
- *Centralized Ticket Management:* All tickets are stored securely in a SQLite database, ensuring easy retrieval and management.

## Installation

To install the QuickTicket library, you can use pip. Open your terminal or command prompt and run the following command:

```bash
pip install quickticket
```

## Usage

### Setting Up QuickTicket

Here’s a quick example of how to set up QuickTicket within your Discord bot. Follow the instructions below to integrate QuickTicket and start managing tickets.

### Example Bot File

``` python
import discord
from discord.ext import commands
from quickticket import QuickTicket

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ticket(ctx):
    """Set up the ticketing system."""
    await QuickTicket.setup(ctx)

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')
```

## Command Breakdown

- `ticket`: This command sets up the ticketing system. When users execute this command, QuickTicket initializes the necessary channels and roles for efficient ticket management.

## Detailed Steps for Usage

1. *Install Dependencies:* Ensure you have all the libraries installed in [requirements.txt](requirements.txt) alongside QuickTicket. If you haven't installed it yet, you can do so by running:

```bash
pip install -r requirements.txt
```

* By copying the requirements.txt

2. *Create a Discord Bot:* If you haven't created a bot yet, visit the [Discord Developer Portal](https://discord.com/developers/applications) to create one. Make sure to enable the necessary permissions and intents.

3. *Add Your Bot to a Server:* Once your bot is set up, invite it to your Discord server using the OAuth2 URL generated in the developer portal.

4. *Run the Bot*: Replace `YOUR_BOT_TOKEN` in the code above with your actual bot token and run your Python script. Use the `!ticket` command in Discord to set up the ticketing system.

## Important Database Warning

| ⚠️ Important: Please do not delete the helper/database.db file. This file is essential for the QuickTicket system to function correctly, as it stores all ticket data. Deleting this file will result in the loss of all ticket information and may cause the bot to malfunction.

## Contributing

We welcome contributions to QuickTicket! If you'd like to help enhance this project, please follow these steps:

1. *Fork the Repository:* Create a personal copy of the repository on GitHub.

2. *Make Changes:* Implement your changes in your forked repository.

3. *Submit a Pull Request:* Share your improvements with the community by submitting a pull request.

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE). For more details, please refer to the [LICENSE](LICENSE) file in the repository.

## Contact

If you have any questions or need support, feel free to reach out to the author:

- Ibrahim 
- Email: [codingstudentbruh@gmail.com](mailto:codingstudentbruh@gmail.com)
- GitHub: [Github](https://github.com/ibrahims-main)

---

## Conclusion

With QuickTicket, managing support tickets on Discord has never been easier. Enjoy the streamlined process and provide your users with the assistance they need in a timely manner. Happy coding!