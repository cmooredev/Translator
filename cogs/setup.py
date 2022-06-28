import discord
from discord.ext import commands
from discord.ui import Select


class Setup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #need to implement setup that lets users configure target lang
        #select = Select()

        print('SetupCog loaded')

    @commands.command()
    async def config(self, ctx):
        select = Select(options=[
            discord.SelectOption(label="English", emoji="🇺🇸", description="English"),
            discord.SelectOption(label="Spanish", emoji="🇪🇸", description="Spanish"),
            discord.SelectOption(label="French", emoji="🇫🇷", description="French"),
        ])
        view = View()
        view.add_item(select)

        await ctx.send("Select what language you would like to translate text to:", view=view)

async def setup(client):
    await client.add_cog(Setup(client))
