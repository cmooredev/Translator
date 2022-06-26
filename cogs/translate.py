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

        #take users information to display in embedded message
        username = str(message.author).split('#')[0]
        user_message = str(message.content)

        #ignore commands
        if user_message[0] == '.':
            return

        #prevent bot from replying to self
        if message.author == self.client.user:
            return

        translator = deepl.Translator(DEEPL_AUTH)
        #translate message into target language
        result = translator.translate_text(user_message, target_lang='EN-US')
        #embedded message with op name and avatar
        #--# TODO: Custom color based on Language? Channel?

        #send embedded message

        await message.channel.send(result)

    @commands.command()
    async def ping(self, ctx):
        await self.client.change_presence(activity=discord.Game('Translating...'))
        await ctx.send('Pong!')

async def setup(client):
    await client.add_cog(Translate(client))
