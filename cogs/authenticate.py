import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pymongo
from datetime import datetime

load_dotenv()
DEEPL_AUTH = os.getenv('DEEPL_AUTH')
MONGO_URI = os.getenv('MONGO_URI')
mongodb_client = pymongo.MongoClient(MONGO_URI)

db = mongodb_client['translatordb']
col = db['api_keys']


class Authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Authenticate loaded')

def auth_apikey(server_id):
    print(f'authenticating....')
    #get server key and check registration date against current date
    server_key = {'server_id': server_id}
    server_access = col.find_one(server_key)

    reg_date = server_access['registration_date']
    to_expired = datetime.now() - reg_date
    credits = server_access['credits']
    print(f'========== {server_id} ==========')
    print(f'{30 - to_expired.days} days left until expired')
    print(f'{credits} are left for the month.')

    if to_expired.days < 0:
        print('Expired key...')
        return False
    if server_access is None:
        print('No server found.')
        return False

    return True


async def setup(client):
    await client.add_cog(Authenticate(client))
