# easy-banking-bot

This is a simple Python Discord bot that uses the discord.py library and allows users to add or remove money from a bank account using commands. The balance is stored in a CSV file.

## Requirements

To use this bot, you'll need:

- Python 3.6 or higher
- discord.py library
- A Discord account and server
- A bot token (obtained from the Discord Developer Portal)

## Installation

1. Clone this repository to your local machine.
2. Install the required packages by running pip install -r requirements.txt in the terminal.
3. In the **bot.py** file, replace *'the-token'* with your bot's token, replace *'YOURCSVFILE.csv'* with the name of your CSV file.
4. Replace the channel IDs in the code with the ID of the channel where you want the bot commands to function.
5. Run the bot by executing python bot.py in the terminal.

## Commands

**?add [amount] [reason]**: Adds the specified amount to the bank account and provides a reason for the deposit.<br>
**?remove [amount] [reason]**: Removes the specified amount from the bank account and provides a reason for the withdrawal.<br>
**?set [amount]**: Sets the bank account balance to the specified amount.<br>
<br>
*Note: Only users with the "Bank" role can use this command.*

## License
This project is licensed under the MIT License. See the LICENSE file for details.
