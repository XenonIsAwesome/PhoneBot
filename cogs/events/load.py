from discord.ext import commands
from discord import TextChannel
from tinydb import TinyDB, Query, where

from util.embedder import welcome_message_embed
from util.db_connection import connect_to_db

db = connect_to_db()


async def insert_guild(guild):
    if db.find_one({'guild_id': guild.id}):
        return

    # Inserting the guild into the database
    db.insert_one({
        "guild_name": guild.name,
        "guild_id": guild.id,
        "admin_roles": [],
        "text_channel_id": "",
        "voice_channel_id": "",
        "friendlist": {},
        "prefix": 'phone.'
    })

    # Sending the welcome message
    for chan in guild.channels:
        if isinstance(chan, TextChannel):
            try:
                return await chan.send('', embed=welcome_message_embed(guild))
            except:
                continue


class _Load(commands.Cog, name="onLoad"):
    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        await insert_guild(guild)

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild):
        db.delete_one({'guild_id': guild.id})


def setup(client):
    global discord_cli
    discord_cli = client
    client.add_cog(_Load(client))
