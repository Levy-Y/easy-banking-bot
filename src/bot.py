import discord
from discord.ext import commands
from discord import app_commands 
import datetime
import sqlite3
import configparser

connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()

bank = None
ranks_ready = False

now = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('./settings/settings.conf')

TOKEN = config.get('TOKEN', 'token')
bank_channel_id = int(config.get('IDS', 'bank_channel_id'))
guild_id = int(config.get('IDS', 'guild_id'))
bank_rank = config.get('RANK_NAME', 'bank_rank')
leader_rank = config.get('RANK_NAME', 'leader_rank')
member_rank = config.get('RANK_NAME', 'member_rank')
embed_title = config.get('EMBED_TITLE', 'embed_title')
announcement_channel_id = int(config.get('IDS', 'announcement_channel_id'))
admin_channel_id = int(config.get('IDS', 'admin_channel_id'))
warn_channel_id = int(config.get('IDS', 'warn_channel_id'))
max_warns = int(config.get('warns', 'max_warns'))
remove_ranks = bool(config.get('warns', 'remove_ranks'))

def log(argument):
    log_filename = now.strftime("console") + ".log"

    with open("./logs/" + log_filename, "a", encoding="UTF-8") as logfile:
        logfile.write(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] {argument}\n')
    

def load_database():
    global bank
    cursor.execute("CREATE TABLE IF NOT EXISTS balance (money INTEGER)")

    cursor.execute("SELECT COUNT(*) FROM balance")
    result = cursor.fetchone()
    count = result[0]

    if count == 0:
        cursor.execute("INSERT INTO balance (money) VALUES (0)")

    cursor.execute("SELECT money FROM balance")
    result = cursor.fetchone()
    bank = result[0]
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS players
                   (discord_id TEXT, ingame_name TEXT, phone_number TEXT, rank TEXT, warn INTEGER DEFAULT 0,
                   PRIMARY KEY (discord_id))''')

    connection.commit()

def save_database(bank):
    cursor.execute("UPDATE balance SET money = ?", (bank,))
    connection.commit()

def add_user(id, name, phone, rank):
    cursor.execute("INSERT OR IGNORE INTO players (discord_id, ingame_name, phone_number, rank) VALUES (?, ?, ?, ?)",
                   (id, name, phone, rank))

    connection.commit()

def update_user(name, phone, rank, id):
    sql_update_query = """
    UPDATE players 
    SET discord_id = ?, ingame_name = ?, phone_number = ?, rank = ?
    WHERE discord_id = ?
    """
        
    cursor.execute(sql_update_query, (name, phone, rank, id))
    connection.commit()

def remove_user(id):
    cursor.execute("DELETE FROM players WHERE discord_id = ?", (id,))
    connection.commit()

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)
        
    load_database()
    
    print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [INFO] Bot Is Ready, current money: ${bank:,}')
    log(f'Bot Is Ready, current money: ${bank:,}')

@bot.tree.command(name="deposit")
@app_commands.describe(amount="enter the amount of money you want to add to the bank")
@app_commands.describe(reason="enter the reason why are you depositing")
async def add(interaction: discord.Interaction, amount: int, reason: str):
    if amount <= 0:
        await interaction.response.send_message(f"The value cannot be negative!", ephemeral=True, delete_after=3)
    else:
        await interaction.response.send_message(f"You added: ${amount} to the bank", ephemeral=True, delete_after=3)
        args = reason.split()
        global bank
        channel = bot.get_channel(bank_channel_id)
        role = discord.utils.get(interaction.user.roles, name=bank_rank)
        if role is not None:
            arg2 = ' '.join(args)
            bank += int(amount)
            embed = discord.Embed(
                title=(f"{embed_title}"),
                description=(
                    f'Current balance: ${bank:,}'
                    f'\nDeposit reason: "{arg2}"'
                ),
                    colour=discord.Colour.dark_grey()
            )
            embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
            print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [BANK] {interaction.user} Added ${amount} to the bank, new balance: ${bank:,}, deposit reason: {arg2}')
            log(f'{interaction.user} Added ${amount:,} to the bank, new balance: ${bank:,}, deposit reason: {arg2}')
            await channel.send(embed=embed)
            save_database(bank)
        else:
            await interaction.response.send_message("You can't edit the balance!", ephemeral=True, delete_after=5)
            
@bot.tree.command(name="withdraw")
@app_commands.describe(amount="enter the amount of money you want to remove from the bank")
@app_commands.describe(reason="enter the reason why are you withdrawing")
async def add(interaction: discord.Interaction, amount: int, reason: str):
    if amount <= 0:
        await interaction.response.send_message(f"The value cannot be negative!", ephemeral=True, delete_after=3)
    else:
        await interaction.response.send_message(f"You removed: ${amount} from the bank", ephemeral=True, delete_after=3)
        args = reason.split()
        global bank
        channel = bot.get_channel(bank_channel_id)
        role = discord.utils.get(interaction.user.roles, name=bank_rank)
        if role is not None:
            arg2 = ' '.join(args)
            bank += int(amount)
            embed = discord.Embed(
                title=(f"{embed_title}"),
                description=(
                    f'Current balance: ${bank:,}'
                    f'\nWithdraw reason: "{arg2}"'
                ),
                    colour=discord.Colour.dark_grey()
            )
            embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
            print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [BANK] {interaction.user} Removed ${amount} from the bank, new balance: ${bank:,}, withdraw reason: {arg2}')
            log(f'{interaction.user} Removed ${amount:,} from the bank, new balance: ${bank:,}, withdraw reason: {arg2}')
            await channel.send(embed=embed)
            save_database(bank)
        else:
            await interaction.response.send_message("You can't edit the balance!", ephemeral=True, delete_after=5)

@bot.tree.command(name="setbalance")
@app_commands.describe(balance="enter the amount of money you want to want to be in the bank")
async def add(interaction: discord.Interaction, balance: int):
    await interaction.response.send_message(f"You set the balance to: ${balance}", ephemeral=True, delete_after=3)
    global bank
    channel = bot.get_channel(bank_channel_id)
    role = discord.utils.get(interaction.user.roles, name=bank_rank)
    if role is not None:
        bank += int(balance)
        embed = discord.Embed(
            title=(f"{embed_title}"),
            description=(
                f'Current balance: ${bank:,}'
            ),
                colour=discord.Colour.dark_grey()
        )
        embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
        print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [BANK] {interaction.user} Set the balance to: ${balance}, new balance: ${bank:,}')
        log(f'{interaction.user} Set the balance to: ${balance}, new balance:  ${bank:,}')
        await channel.send(embed=embed)
        save_database(bank)
    else:
        await interaction.response.send_message("You can't edit the balance!", ephemeral=True, delete_after=5)

@bot.tree.command(name="addtoserver")
@app_commands.describe(id="enter the user ID of the person you want to add")
@app_commands.describe(name="enter the ingame name of the person you want to invite")
@app_commands.describe(phone="enter the ingame phone number of the person you want to invite")
@app_commands.describe(rank="enter the rank you want the person to have")
@app_commands.describe(invite="do you want to send an invite link to the person?")
async def invite(interaction: discord.Interaction, id: str, name: str, phone: str, rank: str, invite: bool = True):
    role = discord.utils.get(interaction.user.roles, name=leader_rank)
    cursor.execute("SELECT * FROM players WHERE discord_id = ?", (id,))
    result = cursor.fetchone()
    if role is not None:
        try:
            user = discord.utils.get(bot.users, id=int(id))
            if user is None:
                await interaction.response.send_message(f"User with `{id}` ID cannot be found", ephemeral=True, delete_after=2)
                return
            if invite == True:
                if result is not None:
                    await interaction.response.send_message(f"User with `{id}` ID is already in the database", ephemeral=True, delete_after=2)
                else:
                    invite_link = await interaction.channel.create_invite(max_uses=1, unique=True)
                    await user.send(invite_link)
                    await interaction.response.send_message(f"Successfully invited `{id}`", ephemeral=True, delete_after=3)
                    log(f'{interaction.user.name} Invited {id} to the server')
                    add_user(id, name, phone, rank)
                    
            elif invite == False:
                if result is not None:
                    await interaction.response.send_message(f"User with `{id}` ID is already in the database", ephemeral=True, delete_after=2)
                else:
                    add_user(id, name, phone, rank)
                    await interaction.response.send_message(f"Successfully added `{id}` to the database", ephemeral=True, delete_after=3)

        except discord.Forbidden:
            await interaction.response.send_message("The user cannot be invited due to their DM privacy settings being turned on", ephemeral=True, delete_after=5)
            log(f'{interaction.user.name} Tried to invite {id} to the server, but the DM attempt was unsuccessful')
        except discord.HTTPException:
            await interaction.response.send_message("This user cannot be invited, either it is a bot profile, or an internal error happened", ephemeral=True, delete_after=5)
            log(f'{interaction.user.name} Tried to invite {id} to the server, but it is a bot profile')
            return
    else:
        await interaction.response.send_message("You don't have the required permissions for that!", ephemeral=True, delete_after=5)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(admin_channel_id)
    id = member.id
    cursor.execute("SELECT rank FROM players WHERE discord_id=?", (str(id),))
    result = cursor.fetchone()

    if result is not None:
        rank = result[0]
        role = discord.utils.get(member.guild.roles, name=rank)
        
        if role:
            await member.add_roles(role)
        else:
            await channel.send(f"{member.name} joined the server, some information isn't correct in the database")
            log(f"{member.name} joined the server, but some information isn't correct in the database")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(admin_channel_id)
    id = member.id
    cursor.execute("SELECT * FROM players WHERE discord_id = ?", (str(id),))
    result = cursor.fetchone()
    if result:
        remove_user(id)
        await channel.send(f"User {member.name} has left the server. Column with member ID `{member.id}` has been removed from the database.")
        log(f"User {member.name} has left the server. Column with member ID {member.id} has been removed from the database.")
    else:
        pass

@bot.tree.command(name="updateuser")
@app_commands.describe(id="enter the user ID of the person you want to edit")
@app_commands.describe(name="enter the ingame name of the person you want to change to")
@app_commands.describe(phone="enter the ingame phone number of the provided person you want to change to")
@app_commands.describe(rank="enter the rank you want the person to have")
async def invite(interaction: discord.Interaction, id: str, name: str, phone: str, rank: str):
    role = discord.utils.get(interaction.user.roles, name=leader_rank)
    if role is not None:
        sql_check_query = "SELECT 1 FROM players WHERE discord_id = ?"
        cursor.execute(sql_check_query, (id,))
        result = cursor.fetchone()
        
        if result:
            update_user(name, phone, rank, id)
            await interaction.response.send_message(f"{interaction.user} changed {id}'s information to: name: {name}, phone: {phone}, rank: {phone}")
            log(f"{interaction.user.name} changed {id}'s information to: name: {name}, phone: {phone}, rank: {phone}")
        else:
            await interaction.response.send_message(f"There isn't a `{id}` in the database", ephemeral=True, delete_after=5)
    else:
        await interaction.response.send_message("You don't have the required permissions for that!", ephemeral=True, delete_after=3)

@bot.tree.command(name="removeuser")
@app_commands.describe(id="enter the user ID of the person you want to edit")
@app_commands.describe(kick="enter True if you want to kick the user as well, and False if you don't want to do that")
async def invite(interaction: discord.Interaction, id: str, kick: str):
    role = discord.utils.get(interaction.user.roles, name=leader_rank)
    if role is not None:
        sql_check_query = "SELECT 1 FROM players WHERE discord_id = ?"
        cursor.execute(sql_check_query, (id,))
        result = cursor.fetchone()

        if result is not None:
            if kick == "False":
                remove_user(id)
                await interaction.response.send_message(f"User with `{id}` ID have been removed from the database", ephemeral=True, delete_after=3)
                log(f'{interaction.user.name} removed user with {id} id from the database')
            elif kick == "True":
                try:
                    guild = interaction.guild
                    member = guild.get_member(int(id))
                    if member is not None:
                        await member.kick(reason="User kicked by command")
                        await interaction.response.send_message(f"User with `{id}` ID has been kicked from the guild", ephemeral=True, delete_after=3)
                        log(f'{interaction.user.name} has kicked user with {id} id from the guild')
                    else:
                        await interaction.response.send_message(f"There isn't a user with `{id}` ID in the guild", ephemeral=True, delete_after=2)
                except discord.Forbidden:
                    await interaction.response.send_message(f"This user cannot be kicked, because they have a higher rank than the bot, either they are the owner of this server, or their rank is more prioritized", ephemeral=True, delete_after=7)
            else:
                await interaction.response.send_message(f"Please choose a valid option (True / False)", ephemeral=True, delete_after=2)
        else:
            await interaction.response.send_message(f"The user with `{id}` ID cannot be found in the database", ephemeral=True, delete_after=2)
    else:
        await interaction.response.send_message(f"You don't have the required permissions for that!", ephemeral=True, delete_after=3)

@bot.tree.command(name='setup')
async def check_roles(interaction: discord.Interaction):
    global ranks_ready
    guild = interaction.guild
    bank_role = discord.utils.get(guild.roles, name=leader_rank)
    leader_role = discord.utils.get(guild.roles, name=leader_rank)
    member_role = discord.utils.get(guild.roles, name=member_rank)
    
    if ranks_ready == False:
        if not bank_role and not leader_role and not member_role:
            bank_role = await guild.create_role(name=bank_rank, colour=discord.Colour.green())
            leader_role = await guild.create_role(name=leader_rank, colour=discord.Colour.blue())
            member_role = await guild.create_role(name=member_rank, colour=discord.Colour.light_grey())
            await interaction.response.send_message('Setup is complete, roles are created!', ephemeral=True, delete_after=3)
            member = interaction.user
            await member.add_roles(bank_role, leader_role)
            ranks_ready = True
            pass
        else:
            await interaction.response.send_message('The roles already exist')
    else:
        await interaction.response.send_message('The roles already exist')

@bot.tree.command(name="announce")
@app_commands.describe(type="enter the type of the announcement (info, important)")
@app_commands.describe(announcement="what would you like to announce")
async def add(interaction: discord.Interaction, type: str, announcement: str):
    info = discord.Colour.blue()
    important = discord.Colour.red()

    channel = bot.get_channel(announcement_channel_id)
    role = discord.utils.get(interaction.user.roles, name=leader_rank)
    if role is not None:
        if type == "info":
            embed = discord.Embed(
                title=(f"Info"),
                description=(
                    f'{interaction.user}`s announcement: "{announcement}"'
                ),
                    colour=info
            )
            embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
            print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [ANNOUNCEMENT] {interaction.user} Announced: `{announcement}`')
            log(f'{interaction.user} Announced: `{announcement}`')
            await channel.send(embed=embed)
            await interaction.response.send_message(f"You have made an announcement!", ephemeral=True, delete_after=2)
        
        elif type == "important":
            embed = discord.Embed(
                title=(f"Important"),
                description=(
                    f'{interaction.user}`s announcement: "{announcement}"'
                ),
                    colour=important
            )
            embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
            print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] [ANNOUNCEMENT] {interaction.user} Announced: `{announcement}`')
            log(f'{interaction.user} Announced: `{announcement}`')
            await channel.send(embed=embed)
            await interaction.response.send_message(f"You have made an announcement!", ephemeral=True, delete_after=2)
        else:
            await interaction.response.send_message('Choose a valid announcement type!', ephemeral=True, delete_after=3)
    else:   
        await interaction.response.send_message("You cannot send announcements!", ephemeral=True, delete_after=5)

@bot.tree.command(name='info')
@app_commands.describe(id="the ID of the user in the guild you want to fetch for in the database")
async def check_roles(interaction: discord.Interaction, id: str):
    cursor.execute("SELECT * FROM players WHERE discord_id = ?", (id,))
    result = cursor.fetchone()
    
    role = discord.utils.get(interaction.user.roles, name=member_rank)
    if role is not None:
        if result is not None:
            await interaction.response.send_message(content=f"Ingame information of user `{id}`: \nName: {result[1]} \nPhone: {result[2]} \nWarns: {result[4]} \nThis message will disapear in 45 seconds!", ephemeral=True, delete_after=45)
        else:
            await interaction.response.send_message(content="The user cannot be found in the team database.", ephemeral=True, delete_after=5)
    else:
        await interaction.response.send_message(content=f"You don't have the required role (Member) to check this.", ephemeral=True, delete_after=5)

@bot.tree.command(name='warn')
@app_commands.describe(id="the ID of the user in the guild you want to warn")
@app_commands.describe(reason="the reason you are giving this user a warn")
async def check_roles(interaction: discord.Interaction, id: str, reason: str):
    channel = bot.get_channel(warn_channel_id)
    user = await bot.fetch_user(id)
    role = discord.utils.get(interaction.user.roles, name=leader_rank)
    cursor.execute("SELECT * FROM players WHERE discord_id = ?", (id,))
    result = cursor.fetchone()
    guild = bot.get_guild(guild_id)
    member = guild.get_member(int(id))
            
    if role is not None:
        if result is not None:
            warn = result[4] + 1
            try:
                cursor.execute("UPDATE players SET warn = ? WHERE discord_id = ?", (warn, id))
                connection.commit()
                if warn == max_warns:
                    roles = member.roles[1:]
                    
                    for role in roles:
                        await member.remove_roles(role)
                        
                    remove_user(id)
                    embed = discord.Embed(
                                title=(f"Warn"),
                                description=(
                                    f'{user.name} reached {max_warns} warns!\n'
                                    f'Last warn reason: "{reason}"\n'
                                    f'Warns: 🔴🔴🔴'
                                    f'Removing all roles'
                                ),
                                    colour=discord.Colour.red()
                            )
                    embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
                    await channel.send(embed=embed)
                    return
                else:
                    indicator = "🔴" * warn + "⚪" * (int(max_warns) - warn)
                    await interaction.response.send_message(content=f"You have warned `{id}`", ephemeral=True, delete_after=5)
                    embed = discord.Embed(
                        title=(f"Warn"),
                        description=(
                            f'{interaction.user} have warned {user.name}\n'
                            f'Reason: "{reason}"\n'
                            f'Warns: ' + indicator
                        ),
                            colour=discord.Colour.red()
                    )
                    embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
                    await channel.send(embed=embed)
            except TypeError:
                await interaction.response.send_message(content=f"You cannot warn this person.", ephemeral=True, delete_after=5)
        else:
            await interaction.response.send_message(content="The user cannot be found in the team database.", ephemeral=True, delete_after=5)
    else:
        await interaction.response.send_message(content=f"You don't have the required role to warn someone.", ephemeral=True, delete_after=5)
    
bot.run(TOKEN)