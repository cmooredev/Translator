import discord
from discord.ext import commands

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="English", emoji="🇺🇸", description="English"),
            discord.SelectOption(label="Spanish", emoji="🇪🇸", description="Spanish"),
            discord.SelectOption(label="French", emoji="🇫🇷", description="French")
        ]
        super().__init__(placeholder="Languages",
            max_values=1, min_values=1, options=options)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 100):
        super().__init__(timeout=timeout)
        self.add_item(Select())

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
    #send select menu to user
    await ctx.send("Select what language you would like to translate text to:", view=SelectView())

async def setup(client):
    await client.add_cog(Setup(client))
