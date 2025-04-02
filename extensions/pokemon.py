import discord
from discord.ext import commands
from discord import app_commands, Embed
from discord.ui import View, Button
import requests

class PokedexView(View):
    """
    Une vue interactive pour afficher les informations d'un Pokémon.
    - Contient deux pages : Informations générales et Statistiques.
    - Récupère les données depuis l'API PokéAPI.
    - Affiche un embed interactif avec des boutons pour naviguer entre les pages.
    - Expire après 1 heure d'inactivité pour économiser les ressources.
    """
    def __init__(self, bot, pokemon_name):
        super().__init__(timeout=3600)  # Timeout de 1 heure
        self.bot = bot
        self.pokemon_name = pokemon_name.lower()
        self.page = 0
        self.message = None  # Stocke le message à modifier

        # Récupération des données
        self.data = self.fetch_data(f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_name}")
        self.species_data = self.fetch_data(f"https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_name}")
        
        self.update_buttons()
    
    def fetch_data(self, url):
        """Récupère les données de l'API et retourne un dictionnaire ou None en cas d'erreur."""
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    
    def generate_embed(self):
        """Génère l'embed correspondant à la page actuelle."""
        return self.create_info_embed() if self.page == 0 else self.create_stats_embed()
    
    def create_info_embed(self):
        """Crée un embed contenant les informations générales du Pokémon."""
        embed = Embed(title=f"{self.data['name'].capitalize()} | N° {self.data['id']}", color=0xE63946)
        embed.set_thumbnail(url=self.data['sprites']['front_default'])
        embed.set_author(name="Pokédex", icon_url="https://i.postimg.cc/1XhgQCcj/541-5418323-gameboy-drawing-electronics-inside-of-a-pokedex-hd-removebg-preview.png")
        
        description = self.get_flavor_text()
        types = self.get_types()
        abilities = self.get_abilities()
        capture_rate = self.species_data.get('capture_rate', 'Inconnu')
        habitat = self.species_data.get('habitat', {}).get('name', 'Inconnu').capitalize()
        egg_groups = self.get_egg_groups()
        
        embed.description = (
            f"### 📜 `Description`\n{description}\n"
            f"### 🔹 `Informations`\n"
            f"**✨ Capacités**: {abilities}\n"
            f"**🎯 Taux de Capture**: {capture_rate}%\n"
            f"**🌍 Habitat**: {habitat}\n"
            f"**🔥 Types**: {types}\n"
            f"### 🪺 `Reproduction`\n"
            f"**🥚 Groupes d'Œufs**: {egg_groups}"
        )
        embed.set_footer(text=f"Pokedex |  Accueil → {self.data['name'].capitalize()}", icon_url=self.data['sprites']['front_default'])
        return embed
    
    def create_stats_embed(self):
        """Crée un embed contenant les statistiques du Pokémon."""
        embed = Embed(title=f"{self.data['name'].capitalize()} | N°{self.data['id']}", color=discord.Color.red())
        embed.set_thumbnail(url=self.data['sprites']['front_default'])
        embed.set_author(name="Pokédex", icon_url="https://i.postimg.cc/1XhgQCcj/541-5418323-gameboy-drawing-electronics-inside-of-a-pokedex-hd-removebg-preview.png")
        
        embed.description = f"{self.get_flavor_text()}\n\n📈 `Statistiques`"
        
        stat_emojis = {
            "hp": "❤️", "attack": "⚔️", "defense": "🛡️", "special-attack": "🔮", "special-defense": "🛡️", "speed": "⚡"
        }
        
        for stat in self.data['stats']:
            name = stat['stat']['name']
            value = stat['base_stat']
            emoji = stat_emojis.get(name, "")
            bar = '<:orange:1356995036776239195>' * (value // 10) + '<:gris:1356995419787231363>' * (15 - (value // 10))
            embed.add_field(name=f"{emoji} {name.capitalize()} ({value})", value=bar, inline=False)

        embed.set_footer(text=f"Pokedex | Statistiques → {self.data['name'].capitalize()}", icon_url=self.data['sprites']['front_default'])
        return embed
    
    def get_flavor_text(self):
        """Retourne la première description du Pokémon en français si disponible, sinon en anglais."""
        for entry in self.species_data['flavor_text_entries']:
            if entry['language']['name'] == 'fr':
                return entry['flavor_text'].replace('\n', ' ')
        return self.species_data['flavor_text_entries'][0]['flavor_text'].replace('\n', ' ')
    
    def get_types(self):
        """Retourne une chaîne contenant les types du Pokémon."""
        return ', '.join(t['type']['name'].capitalize() for t in self.data['types'])
    
    def get_abilities(self):
        """Retourne une chaîne contenant les capacités du Pokémon."""
        return ', '.join(a['ability']['name'].capitalize() for a in self.data['abilities'])
    
    def get_egg_groups(self):
        """Retourne une chaîne contenant les groupes d'œufs du Pokémon."""
        egg_groups = [egg_group['name'].capitalize() for egg_group in self.species_data.get('egg_groups', [])]
        return ', '.join(egg_groups) if egg_groups else 'Inconnu'
    
    async def update_message(self):
        """Met à jour l'embed affiché avec la page actuelle."""
        self.update_buttons()
        if self.message:
            await self.message.edit(embed=self.generate_embed(), view=self)
    
    def update_buttons(self):
        """Met à jour les boutons de navigation."""
        self.clear_items()
        buttons = [
            ("Accueil", "🏠", 0),
            ("Statistiques", "📊", 1)
        ]
        
        for label, emoji, page_index in buttons:
            button = Button(label=label, style=discord.ButtonStyle.danger, emoji=emoji, disabled=self.page == page_index)
            button.callback = lambda interaction, idx=page_index: self.change_page(interaction, idx)
            self.add_item(button)
    
    async def change_page(self, interaction: discord.Interaction, page_index):
        """Change de page si l'utilisateur est le bon."""
        self.page = page_index
        await interaction.response.defer()
        await self.update_message()
    
    async def on_timeout(self):
        """Quand la vue expire après 1h, elle est supprimée pour économiser les ressources."""
        if self.message:
            await self.message.edit(view=None)

class PokedexGroup(app_commands.Group):
    """Groupe de commandes pour le Pokédex."""
    def __init__(self, bot):
        super().__init__(name="pokedex", description="Groupe de commandes du Pokédex")
        self.bot = bot

    @app_commands.command(name="pokemon", description="Obtenez des informations sur un Pokémon.")
    async def pokemon(self, interaction: discord.Interaction, pokemon_name: str):
        await interaction.response.defer()
        view = PokedexView(self.bot, pokemon_name)

        if view.data and view.species_data:
            message = await interaction.followup.send(embed=view.generate_embed(), view=view)
            view.message = message
        else:
            await interaction.followup.send(f"❌ Pokémon inconnu: '{pokemon_name}'.", ephemeral=True)

async def setup(bot: commands.Bot):
    bot.tree.add_command(PokedexGroup(bot))
