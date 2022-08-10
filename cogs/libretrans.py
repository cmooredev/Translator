import discord
from discord.ext import commands
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("http://127.0.0.1:5000")

def free_trans(message, lang):
    tr_lang = lang.lower()
    print(f'my message:  {message}')
    translation = lt.translate(message, "auto", tr_lang)
    print(translation)
    return translation

class Libretrans(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('LibretransCog loaded')

    


async def setup(client):
    await client.add_cog(Libretrans(client))
