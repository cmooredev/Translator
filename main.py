import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

def get_prefix(client, message):

client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('Bot is online')

@client.command()
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{filename[:-3]} loaded.')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=25):
    await ctx.channel.purge(limit=amount)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())
