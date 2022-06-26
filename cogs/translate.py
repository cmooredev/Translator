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
        user_message = str(message.content)

        #ignore commands
        if user_message[0] == '.':
            return

        #prevent bot from replying to self
        if message.author == self.client.user:
            return

        if 'Translate' in str(message.author.roles):
            translator = deepl.Translator(DEEPL_AUTH)
            #translate message into target language
            result = translator.translate_text(user_message, target_lang='EN-US')
            if result.detected_source_lang != 'EN' and result.detected_source_lang != 'EN-US' :
                #embedded message with op name and avatar
                #--# TODO: Custom color based on Language? Channel?
                embed=discord.Embed(description=result)
                #displays user avatar
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
                await message.channel.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

async def setup(client):
    await client.add_cog(Translate(client))
