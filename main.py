__author__ = "Xenon#0239"

# discord.py
import discord
from discord.ext import commands

# setup .env file
from env_file import load as dotenv
from util.misc import walk_cogs

# setup logging and other imports
import logging
import os

# local imports
from util.db_management.db_connection import connect_to_db
from util.db_management.db_sync import sync_with_db

dotenv('.env')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='phonebot.log', encoding='utf-8', mode='w')
consoleHandler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger.addHandler(consoleHandler)

with open('owners.txt', 'r') as f:
    OWNERS = f.read().split('\n')

db = connect_to_db()

# setup bot
intents = discord.Intents.default()
intents.guilds = True
intents.reactions = True


def get_prefix(client, message):
    if q := db.find_one({'guild_id': message.guild.id}):
        if prefix := q.get('prefix'):
            return prefix
    return 'phone.'


client = commands.Bot(command_prefix=get_prefix, intents=intents)


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}! | Running as {os.getenv("NAME")}V{os.getenv("VERSION")}')
    logger.info("Invite link: https://discord.com/api/oauth2/authorize?client_id=757545767236927529&permissions=3157072&scope=bot")

    # load all the cogs when the bot starts
    for filename in walk_cogs('cogs'):
        client.load_extension(filename)

    logger.info(f'Operating in {len(client.guilds)} discord servers')

    await sync_with_db(client)


@client.command()
async def load(ctx, extension):
    if str(ctx.message.author.id) in OWNERS:
        try:
            client.load_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send(f'**Error:** Could not load the `{extension}` cog\n{e}')
    else:
        await ctx.send('Only the owner can do that...')


@client.command()
async def unload(ctx, extension):
    if str(ctx.message.author.id) in OWNERS:
        try:
            client.unload_extension(f'cogs.{extension}')
        except Exception as e:
            print(e)
            await ctx.send(f'**Error:** Could not unload the `{extension}` cog\n{e}')
    else:
        await ctx.send('Only the owner can do that...')


@client.command()
async def shutdown(ctx):
    if str(ctx.message.author.id) in OWNERS:
        try:
            await client.close()
        except:
            exit()
    else:
        await ctx.send('Only the owner can do that...')


@client.command()
async def cogs(ctx):
    if str(ctx.message.author.id) in OWNERS:
        msg = "```\n"
        msg += '\n'.join(walk_cogs('cogs')).replace('cogs.', '')
        msg += "```"
        await ctx.send(msg)
    else:
        await ctx.send('Only the owner can do that...')


if __name__ == "__main__":
    client.run(os.getenv('TOKEN'))
