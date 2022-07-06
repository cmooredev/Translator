import discord
import os
import deepl
from discord.ext import commands
from dotenv import load_dotenv
from lingua import Language, LanguageDetectorBuilder
import pymongo

languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

load_dotenv()
DEEPL_AUTH = os.getenv('DEEPL_AUTH')
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)

db = mongodb_client["translatordb"]
col = db["server_lang"]

languages = {
    'french':'FR',
    'english':'EN-US',
    'spanish':'ES',
}

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

        #ignore emojis
        if user_message[0] == ':':
            return
        #ignore custom emojis
        if user_message[0] == '<':
            return

        #ignore urls
        if user_message[:4] == 'http':
            return

        #prevent bot from replying to self
        if message.author == self.client.user:
            return

        server_key = {'server_id': message.guild.id}
        lang = col.find_one(server_key)
        server_lang = lang['target_lang']

        if 'Translate' in str(message.author.roles):
            lingua_result = detector.detect_language_of(user_message)
            #hard coded target language, need to move to variable
            lingua_lang = lingua_result.name
            len_chars = len(user_message)

            if lingua_lang.lower() != server_lang.lower():

                #check for counter and increment
                counter_exits = lang.get('counter')
                if counter_exits == None:
                    print('NO COUNTER')
                    specs = {
                        "counter" : len_chars,
                    }
                    #add counter if it doesnt exist
                    result = col.update_one(server_key, {'$set':specs}, True)
                else:
                    print('UPDATED COUNTER')
                    #increment counter
                    result = col.update_one(server_key, {'$inc': {'counter': len_chars}})

                translator = deepl.Translator(DEEPL_AUTH)
                #translate message into target language
                result = translator.translate_text(user_message, target_lang=languages[server_lang])
                #if translation results in same message
                if str(user_message) == str(result):
                    print("No translation found.")
                    return
                #embedded message with op name and avatar
                #--# TODO: Custom color based on Language? Channel?
                embed=discord.Embed(description=result)
                #displays user avatar
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
                await message.channel.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        server_key = {'server_id': ctx.guild.id}
        lang = col.find_one(server_key)
        result = lang['target_lang']
        await ctx.send(f'Current target language: {result}')

async def setup(client):
    await client.add_cog(Translate(client))
