import discord
from discord import app_commands
from discord.ext import commands, tasks
import pymongo
from dotenv import load_dotenv
import os
import time
import asyncio
from datetime import datetime
from datetime import timedelta

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)
db = mongodb_client["translatordb"]
col = db["api_keys"]

#select menu for choosing a target language
class SelectLanguage(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="bulgarian", emoji="🇧🇬", description="bulgarian - not available in free mode"),
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
            discord.SelectOption(label="lithuanian", emoji="🇱🇹", description="lithuanian - not available in free mode"),
            discord.SelectOption(label="latvian", emoji="🇱🇻", description="latvian - not available in free mode"),
            discord.SelectOption(label="portuguese", emoji="🇵🇹", description="portuguese"),
            discord.SelectOption(label="polish", emoji="🇵🇱", description="polish"),
            discord.SelectOption(label="spanish", emoji="🇪🇸", description="spanish"),
            discord.SelectOption(label="slovak", emoji="🇸🇰", description="slovak"),
            discord.SelectOption(label="slovenian", emoji="🇸🇮", description="slovenian - not available in free mode"),
            discord.SelectOption(label="turkish", emoji="🇹🇷", description="turkish"),
            discord.SelectOption(label="russian", emoji="🇷🇺", description="russian"),
            discord.SelectOption(label="romanian", emoji="🇷🇴", description="romanian  - not available in free mode"),

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

        server_access = col.find_one(specs)
        if server_access is None:
            specs = {
                "server_id" : server_id,
                "key": 1000,
                "registration_date": datetime.now() - timedelta(days=1),
                "credits": 1000,
            }

        server_key = {"server_id" : server_id}
        #update server info
        result = col.update_one(server_key, {'$set':specs}, True)
        result = col.update_one(server_key, {'$set': {f"user_langs.{user_id}": user_choice}}, True)


        ## retrieve a user's lang
        #user_lang = col.find_one(server_key)
        #user_lang = user_lang['user_langs'][f'{user_id}']['lang']

        await interaction.response.send_message(content=f"Language selected.", ephemeral=True)
        self.stop()

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 10):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())

class Setup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(seconds=600.0)
    async def change_status(self):
        print('bg')
        #await self.client.change_presence(activity=discord.Game('.speakyhelp'))

    @commands.Cog.listener()
    async def on_ready(self):
        #need to implement setup that lets users configure target lang
        #select = Select()
        #load initial settings here
        #########
        await self.bot.wait_until_ready()
        self.change_status.start()
        print('SetupCog loaded')

   
    @app_commands.command(description='Select the language you would like your text translated into.')
    #@commands.has_permissions(administrator = True)
    async def setlang(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name="Translate")
        if role is None:
            role = await interaction.guild.create_role(name="Translate", colour=discord.Colour.blue())
        await interaction.user.add_roles(role)
        select_view = SelectView()
        #msg = await interaction.channel.send("User must have role 'Translate' for bot to translate their text.\nSelect language\nMenu will delete in 12s", view=select_view, delete_after=12)
        await interaction.response.send_message("Choose a language", view=select_view, ephemeral=True)

    @app_commands.command(description='Help menu for SpeakyBot.')
    async def speakyhelp(self, interaction: discord.Interaction):
        result = '**Commands(Slash Commands)**\
                \n\n`/setlang` -> sets language for using interacting with select menu \
                \nThis will also give you the Translate role.  To stop translations, remove this role.  \
                \n\n`/stats` -> check current credits for paid services \
                \n\n`/untranslate` -> Remove the translate role \
                \n\n**Required Role**\
                \nUsers must have the translate role in order for the bot to recognize them.\
                \n\nYou can use unlimited free translations when you run out of paid credits.  The free translator\
                will be marked with a red bar on the left of the embed message.\
                \n\n**Purchase Credits**\
                *www.hellabots.com*'
        embed=discord.Embed(description=result)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(description='Remove translation role and stop translating your messages.')
    async def untranslate(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name="Translate")
        if role is None:
            return
        await interaction.user.remove_roles(role)
        await interaction.response.send_message("Translate role has been removed.", ephemeral=True)


    @commands.command()
    @commands.is_owner()
    async def reload_cogs(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.bot.reload_extension(f'cogs.{filename[:-3]}')
        await ctx.send('Cogs reloaded.')

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(
          f"Synced {len(fmt)} commands."
        )
        return

async def setup(bot):
    await bot.add_cog(Setup(bot))
