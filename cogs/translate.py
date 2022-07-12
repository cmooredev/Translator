import discord
import os
import deepl
import json
from discord.ext import commands
from dotenv import load_dotenv
from lingua import Language, LanguageDetectorBuilder
import pymongo
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

from .authenticate import auth_apikey
from .languages import lingua_languages


detector = LanguageDetectorBuilder.from_languages(*lingua_languages).build()

load_dotenv()
#deepl credentials
DEEPL_AUTH = os.getenv('DEEPL_AUTH')

#mongodb credentials
MONGO_URI = os.getenv('MONGO_URI')

#google translate credentials
GOOGLE_AUTH = json.loads(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
GOOGLE_AUTH['private_key'] = GOOGLE_AUTH['private_key'].replace('\\n', '\n')
CREDENTIALS = service_account.Credentials.from_service_account_info(GOOGLE_AUTH)
gtranslate_client = translate.Client(credentials=CREDENTIALS)

mongodb_client = pymongo.MongoClient(MONGO_URI)

db = mongodb_client["translatordb"]
col = db["server_lang"]

sub_col = db["api_keys"]

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

        print(gtranslate_client.translate('hola mis amigos', target_language='en'))

        print('TranslatorCog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        #prevent bot from replying to self
        if message.author == self.client.user:
            return

        server_id = message.guild.id
        #authenticate api key
        if auth_apikey(server_id) == False:
            return

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

        server_key = {'server_id': server_id}
        lang = col.find_one(server_key)
        server_sub = sub_col.find_one(server_key)
        server_credits = server_sub['credits']
        server_lang = lang['target_lang']


        if 'Translate' in str(message.author.roles):
            lingua_result = detector.detect_language_of(user_message)
            #hard coded target language, need to move to variable
            lingua_lang = lingua_result.name
            print(lingua_lang)
            len_chars = len(user_message)

            if lingua_lang.lower() != server_lang.lower():

                #server credits
                print('UPDATED COUNTER')
                #increment counter
                result = sub_col.update_one(server_key, {'$inc': {'credits': -1*len_chars}})

                translator = deepl.Translator(DEEPL_AUTH)
                #translate message into target language
                result = translator.translate_text(user_message, target_lang=languages[server_lang])
                #if translation results in same message
                if str(user_message) == str(result):
                    print(f"No translation found. ---- {result}")
                    return
                #embedded message with op name and avatar
                #--# TODO: Custom color based on Language? Channel?
                embed=discord.Embed(description=result)
                #displays user avatar
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
                await message.channel.send(embed=embed)


    @commands.command()
    async def trstats(self, ctx):
        server_key = {'server_id': ctx.guild.id}
        lang = col.find_one(server_key)
        result = lang['target_lang']
        server_credits = sub_col.find_one(server_key)
        current_credits = server_credits['credits']
        await ctx.send(f'Current target language: {result} Credits: {current_credits}')

async def setup(client):
    await client.add_cog(Translate(client))
