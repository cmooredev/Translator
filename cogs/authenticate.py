import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
DEEPL_AUTH = os.getenv('DEEPL_AUTH')
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)

db = mongodb_client["translatordb"]
col = db["api_keys"]


class Authenticate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Authenticate loaded')

def auth_apikey(server_id):
    print('authenticating....')
    server_key = {'server_id': server_id}
    server_access = col.find_one(server_key)
    print(server_id)
    print(server_access)
    print(f'........ has access')
    return True

async def setup(client):
    await client.add_cog(Authenticate(client))
