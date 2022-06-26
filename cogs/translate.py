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
        username = str(message.author).split('#')[0]
        user_message = str(message.content)

        if message.author == self.client.user:
            return

        translator = deepl.Translator(DEEPL_AUTH)
        result = translator.translate_text(user_message, target_lang='EN-US')
        embed=discord.Embed(title=message.author.display_name,
        description=result, color=0xFF5733)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        await message.channel.send(message.author.mention)

    @commands.command()
    async def ping(self, ctx):
        await self.client.change_presence(activity=discord.Game('Translating...'))
        await ctx.send('Pong!')

async def setup(client):
    await client.add_cog(Translate(client))

    if message.author == self.client.user:
        return
