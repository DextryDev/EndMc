import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix="/", description="Bot de prévisions météo", intents=discord.Intents.all(), help_command=None)

#Recherche des informations requises pour les API (Discord.py)
with open('config.json', 'r') as f:
    config = json.load(f)
    token = config['Discord']['Token']

@bot.event
async def on_ready() -> None:
    # Recherche des extensions
    print(color.BLUE + "[Loader] Chargement des extensions...")
    for nom_fichier in os.listdir("extensions"):
        if nom_fichier.endswith(".py"):
            extension_name = nom_fichier[:-3]
            await bot.load_extension(f'extensions.{extension_name}')
            print(color.BLUE +f"[Loader] Chargement de l'extension {extension_name}...")

    print(color.BLUE + "[Loader] Chargement des extensions terminé !")
    
    #Syncronisation des commandes
    await bot.tree.sync()
    print(f'[Power][On] {bot.user.name} est désormé votre service...')


class color():
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WHITE = '\033[0m'
    MAGENTA = '\033[95m'
    GRIS = '\033[90m'