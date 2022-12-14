import discord
from discord.ext import commands
import csv
import datetime

TOKEN = 'the-token'

bot = commands.Bot(command_prefix='?', intents = discord.Intents.all())

bank = 0

def save_balance():
    with open('YOURCSVFILE.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([bank])

def load_balance():
    global bank
    with open('YOURCSVFILE.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            bank = int(row[0])

@bot.event
async def on_ready():
    load_balance()
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] Bot Is Ready, current money: ${bank:,}')

@bot.command(pass_context=True)
async def add(ctx, arg, *args):
    channel = bot.get_channel(123456789)
    global bank
    role = discord.utils.get(ctx.guild.roles, name="Bank")
    if role in ctx.author.roles:
        if not arg.isdigit():
            await ctx.send("Számot adj meg kérlek!", delete_after=2)
            await ctx.message.delete()
            return
        elif arg.isdigit():
            arg2 = ' '.join(args)

            bank = int(arg) + bank
            embed = discord.Embed(
                title=("Continental Bank"),
                description=(
                    f'Félretett pénz jelenleg: ${bank:,}'
                    f'\nHozzáadás indoka: "{arg2}"'
                    ),
                colour=discord.Colour.dark_grey()
            )
            now = datetime.datetime.now()
            embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
            arg = int(arg)
            print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] {ctx.message.author.name} Added ${arg:,} to the bank, new balance: ${bank:,}, hozzáadás indoka: {arg2}')

            await channel.send(embed=embed)
            await ctx.message.delete()
            save_balance()
    else:
        await ctx.send("Nem nyúlhatsz bele a kasszába!", delete_after=5)
        await ctx.message.delete()

@bot.command(pass_context=True)
async def remove(ctx, arg, *args):
    channel = bot.get_channel(123456789)
    global bank
    role = discord.utils.get(ctx.guild.roles, name="Bank")
    if role in ctx.author.roles:
        if not arg.isdigit():
            await ctx.send("Számot adj meg kérlek!", delete_after=2)
            await ctx.message.delete()
            return
        elif arg.isdigit():
            arg2 = ' '.join(args)
            if bank - int(arg) == 0 or bank - int(arg) > 0:
                bank = bank - int(arg)
                embed = discord.Embed(
                    title=("Continental Bank"),
                    description=(
                        f'Félretett pénz: ${bank:,}'
                        f'\nKivétel indoka: "{arg2}"'
                        ),
                    colour=discord.Colour.dark_grey()
                )
                now = datetime.datetime.now()
                embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))
                arg = int(arg)
                print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] {ctx.message.author.name} Removed ${arg:,} from the bank, new balance: ${bank:,}, kivétel indoka: {arg2}')

                await channel.send(embed=embed)
                await ctx.message.delete()
                save_balance()
            elif bank - int(arg) < 0:
                await ctx.send("Nem tudsz ennyit kivonni!", delete_after=2)
                await ctx.message.delete()
    else:
        await ctx.send("Nem nyúlhatsz bele a kasszába!", delete_after=5)
        await ctx.message.delete()

@bot.command(pass_context=True)
async def set(ctx, arg):
    channel = bot.get_channel(123456789)
    global bank
    role = discord.utils.get(ctx.guild.roles, name="Bank")
    if role in ctx.author.roles:
        try:
            value = int(arg)

            if value % 1 == 0 and value >= 0:
                bank = value
                embed = discord.Embed(
                    title=("Continental Bank"),
                    description=(
                        f'Félretett pénz: ${bank:,}'),
                    colour=discord.Colour.dark_grey()
                )
                now = datetime.datetime.now()
                embed.set_footer(text=now.strftime("%Y-%m-%d %H:%M:%S"))

                print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] {ctx.message.author.name} Set the bank balance to ${value:,}')

                await channel.send(embed=embed)
                await ctx.message.delete()
                save_balance()
            elif value < 0:
                await ctx.send("Nem lehet minusz az érték!", delete_after=2)
                await ctx.message.delete()
        except ValueError:
                await ctx.send("Számot adj meg kérlek!", delete_after=2)
                await ctx.message.delete()
    else:
        await ctx.send("Nem nyúlhatsz bele a kasszába!", delete_after=5)
        await ctx.message.delete()

bot.run(TOKEN)
