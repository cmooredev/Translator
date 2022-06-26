import discord
from discord.ext import commands
from discord.ui import Select


class Setup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('SetupCog loaded')

async def setup(client):
    await client.add_cog(Setup(client))
