import discord
from discord.ext import commands
import json
import os
import datetime


with open('config.json', 'r') as f:
    config = json.load(f)
    TOKEN = config['discord']['token']
    f.close()

bot = commands.Bot(command_prefix="/", description="EndMC", intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print("[Chargement] Chargement des extensions...")

    for nom_fichier in os.listdir("extensions"):
        if nom_fichier.endswith(".py"):
            extension_name = nom_fichier[:-3]
            try:
                await bot.load_extension(f'extensions.{extension_name}')
                print(f" [Chargement] Chargement de l'extension {extension_name}...")
            except Exception as e:
                print(f" [Chargement] Erreur lors du chargement de l'extension {extension_name}: {e}")

    await bot.tree.sync()

    print(f'{bot.user.name} est prêt pour etre utiliser ! ') 

    await bot.change_presence(activity=discord.Game(name="Pokemon"))
    


bot.run(token=TOKEN)
