# RP Server Assistant

RP Server Assistant is a feature-rich Python Discord bot built on the discord.py library. The bot offers a comprehensive set of functionalities, including bank account management, user database maintenance, announcement sending, and a warn system powered by slash commands. All user balances and data are securely stored in a SQLite database.

## Requirements

Before using this bot, ensure you have the following:

- Python 3.6 or higher
- discord.py library
- A Discord account and server
- A bot token (obtained from the [Discord Developer Portal](https://discord.com/developers/applications))

## Installation

Follow these steps to set up the bot:

1. Clone this repository to your local machine.
2. Install the required packages by running the **install.bat** file provided in the *install* folder.
3. In the **/settings/settings.conf** file, update the necessary values to match your server's configuration.
4. Run the bot by executing `python bot.py` in the terminal.

TODO: In the future, a Dockerfile will be provided to simplify running the bot on any Linux/Windows machine.

## Commands

Here are the commands available for the bot:

- **/setup**: Initializes the server roles with predefined names and grants the user running the command the "Bank" and "Leader" roles. This command can only be executed once during setup.

- **/addtoserver [id] [ingame name] [ingame phone] [rank] [should invite]**: Invites a Discord user (using their Discord ID) to the server and adds their information to the database. The command allows specifying the user's in-game name, in-game phone number, rank, and whether to send an invitation to them.

- **/info [id]**: Retrieves and displays all available information about a user from the database based on their user ID.

- **/removeuser [id] [should kick]**: Removes a user's data from the database. If the "should kick" option is true, the bot will also kick the user from the server.

- **/updateuser [id] [ingame name] [ingame phone] [rank] [should invite]**: Updates a user's information in the database based on their user ID. The command allows modifying their in-game name, in-game phone number, rank, and invitation status.

- **/warn [id] [reason]**: Issues a warning to a user identified by their user ID. If a user accumulates the preconfigured maximum number of warnings, the bot will automatically remove all roles from the user, provided the "remove_ranks" option in the configuration is set to true.

- **/deposit [amount] [reason]**: Deposits a specified amount of money into the bank.

- **/withdraw [amount] [reason]**: Withdraws a specified amount of money from the bank.

- **/set [amount]**: Sets the bank balance to a specific amount.

*Note: The "Bank" role is required to execute the balance-related commands, and the "Leader" role is needed to perform admin commands.*

## Logging

The RP Server Assistant bot includes a robust logging system to track and record important events and activities within the server. This feature helps server administrators and moderators keep a detailed record of various interactions and activities performed by the users and the bot itself.

### How Logging Works

The logging function captures essential events such as user joins, leaves, warns, and other significant commands executed by users with the "Leader" role. Additionally, it logs successful and failed attempts at modifying user data, such as updating user information, adding or removing money, and performing administrative actions.

### Accessing Logs

The log entries are stored in a separate log file, which is continuously updated as events occur. Server administrators can access and review these logs to gain insights into user interactions and bot activities.

## License

This project is licensed under the MIT License. Refer to the LICENSE file for more details.
