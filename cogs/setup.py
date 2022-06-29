import discord
from discord.ext import commands
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)
db = mongodb_client["translatordb"]
col = db["target_lang"]

#select menu for choosing a target language
class SelectLanguage(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="English", emoji="🇺🇸", description="English"),
            discord.SelectOption(label="Spanish", emoji="🇪🇸", description="Spanish"),
            discord.SelectOption(label="French", emoji="🇫🇷", description="French")
        ]
        super().__init__(placeholder="Languages",
            max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        print(interaction.guild.id)
        specs = {"target_lang" : self.values[0]}
        result = col.insert_one(specs)
        await interaction.response.send_message(content=f"Your choice is {self.values[0]}", ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 100):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())

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
