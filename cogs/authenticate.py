import discord
from discord.ext import commands

class Authenticate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Authenticate loaded')

def auth_apikey():
    print('authenticating....')

async def setup(client):
    await client.add_cog(Authenticate(client))
