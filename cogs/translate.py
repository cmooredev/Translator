import discord
import os
import deepl
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DEEPL_AUTH = os.getenv('DEEPL_AUTH')

class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('TranslatorCog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        

    @commands.command()
    async def ping(self, ctx):
        await self.client.change_presence(activity=discord.Game('Translating...'))
        await ctx.send('Pong!')

async def setup(client):
    await client.add_cog(Translate(client))
