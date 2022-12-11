import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Loading balance file...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hali {interaction.user.mention}!", ephemeral = True)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "Mit mondjak?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

bot.run("MTA1MTU3MjM1MjA5NTM2MzA4Mg.Gjm0-U.R940C76tTeqYZBff9VG3UOOpCnNGeitgPBLHdY")
