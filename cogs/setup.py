import discord
from discord.ext import commands
import pymongo
from dotenv import load_dotenv
import os
import time
import asyncio

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)
db = mongodb_client["translatordb"]
col = db["api_keys"]

#select menu for choosing a target language
class SelectLanguage(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="bulgarian", emoji="🇧🇬", description="bulgarian"),
            discord.SelectOption(label="czech", emoji="🇨🇿", description="czech"),
            discord.SelectOption(label="chinese", emoji="🇨🇳", description="chinese"),
            discord.SelectOption(label="dutch", emoji="🇷🇺", description="dutch"),
            discord.SelectOption(label="danish", emoji="🇩🇰", description="danish"),
            discord.SelectOption(label="english", emoji="🇺🇸", description="english"),
            discord.SelectOption(label="estonian", emoji="🇪🇪", description="estonian"),
            discord.SelectOption(label="finnish", emoji="🇫🇮", description="finnish"),
            discord.SelectOption(label="french", emoji="🇫🇷", description="french"),
            discord.SelectOption(label="german", emoji="🇩🇪", description="german"),
            discord.SelectOption(label="greek", emoji="🇬🇷", description="greek"),
            discord.SelectOption(label="hungarian", emoji="🇭🇺", description="hungarian"),
            discord.SelectOption(label="indonesian", emoji="🇮🇩", description="indonesian"),
            discord.SelectOption(label="italian", emoji="🇮🇹", description="italian"),
            discord.SelectOption(label="japanese", emoji="🇯🇵", description="japanese"),
            discord.SelectOption(label="lithuanian", emoji="🇱🇹", description="lithuanian"),
            discord.SelectOption(label="latvian", emoji="🇱🇻", description="latvian"),
            discord.SelectOption(label="portuguese", emoji="🇵🇹", description="portuguese"),
            discord.SelectOption(label="polish", emoji="🇵🇱", description="polish"),
            discord.SelectOption(label="spanish", emoji="🇪🇸", description="spanish"),
            discord.SelectOption(label="slovak", emoji="🇸🇰", description="slovak"),
            discord.SelectOption(label="slovenian", emoji="🇸🇮", description="slovenian"),
            discord.SelectOption(label="turkish", emoji="🇹🇷", description="turkish"),
            discord.SelectOption(label="russian", emoji="🇷🇺", description="russian"),
            discord.SelectOption(label="romanian", emoji="🇷🇴", description="romanian"),

        ]
        super().__init__(placeholder="Languages",
            max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        #get server id to store specific target languages for multiple servers
        chosen_lang = self.values[0]
        user_id = interaction.user.id
        user_choice =  {
            "lang": chosen_lang,
            "user_id": user_id
        }

        server_id = interaction.guild.id
        specs = {
            "server_id" : server_id,
        }

        server_key = {"server_id" : server_id}
        #update server info
        result = col.update_one(server_key, {'$set':specs}, True)
        result = col.update_one(server_key, {'$set': {f"user_langs.{user_id}": user_choice}}, True)


        ## retrieve a user's lang
        #user_lang = col.find_one(server_key)
        #user_lang = user_lang['user_langs'][f'{user_id}']['lang']

        await interaction.response.send_message(content=f"{chosen_lang}", ephemeral=True)
        self.stop()

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 10):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())

class Setup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #need to implement setup that lets users configure target lang
        #select = Select()
        #load initial settings here
        #########
        print('SetupCog loaded')

    @commands.command()
    #@commands.has_permissions(administrator = True)
    async def setlang(self, ctx, *args):
        select_view = SelectView()
        msg = await ctx.send("Select language\nMenu will delete in 12s", view=select_view, delete_after=12)

    @commands.command()
    async def speakyhelp(self, ctx):
        result = '.setlang -> sets language for using interacting with select menu \
                \n .stats -> check current credits and time until expiration \
                \n You must create a role called Translate and give it to each \
                member that you would like to be translated.  Each user can select \
                their own language to translate into.'
        embed=discord.Embed(description=result)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Setup(client))
