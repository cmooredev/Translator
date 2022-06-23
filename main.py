import discord
import config
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('Bot is online')

client.run(config.KEY)
