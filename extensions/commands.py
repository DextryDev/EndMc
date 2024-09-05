import discord
from discord.ext import commands
from discord import app_commands
from build.embed import EmbedBuilder
from build.pokerequest import PokeInfo

class Pokedex(app_commands.Group):
    def __init__(self, bot: commands.bot) -> None:
        super().__init__(name="Pokedex", description="Commandes en rapport avec le pokedex.")
        self.bot = bot

    @app_commands.command(name="pokemon", description="Permet de recueillir des information à propos d'un pokémon.")
    async def pokemon(self, PokemonName: str) -> None:
        pass


class CogCommandes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CogCommandes(bot))
    await bot.add_command(PokeInfo(bot))