import discord
from discord.ext import commands

basic_languages = {
    'french':'FR',
    'english':'EN-US',
    'spanish':'ES',
    'bulgarian': 'BG',
    'czech': 'CZ',
    'danish': 'DA',
    'german': 'DE',
    'greek': 'EL',
    'estonian': 'ET',
    'finnish': 'FT',
    'hungarian': 'HU',
    'italian': 'IT',
    'japanese': 'JA',
    'lithuanian': 'LT',
    'latvian': 'LV',
    'dutch': 'NL',
    'polish': 'PL',
    'portuguese': 'PT-PT',
    'romanian': 'RO',
    'russian': 'RU',
    'slovak': 'SK',
    'slovenian': 'SL',
    'turkish': 'TR',
    'swedish': 'SV',
    'chinese': 'ZH',
    'indonesian': 'IN',
}



class Languages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Languages loaded')


async def setup(client):
    await client.add_cog(Languages(client))
