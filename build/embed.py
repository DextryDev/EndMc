from datetime import datetime
from typing import *
import discord

class EmbedBuilder(discord.Embed):
    def __init__(self, *, colour: int | discord.Colour | None = None, color: int | discord.Colour | None = None, title: Any | None = None, type: Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = 'rich', url: Any | None = None, description: Any | None = None, timestamp: datetime | None = None):
        super().__init__(colour=colour, color=color, title=title, type=type, url=url, description=description, timestamp=timestamp)