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
    print(f'authenticating....{server_id}')
    server_key = {'server_id': server_id}
    server_access = col.find_one(server_key)
    if server_access != None:
        return True
        print(f'{server_key}...... has access')
    else:
        print('access denied')
        return False


async def setup(client):
    await client.add_cog(Authenticate(client))
