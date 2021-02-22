from discord.ext import commands

from util.db_management.db_connection import connect_to_db
from util.db_management.db_sync import insert_guild, remove_guild

db = connect_to_db()


class _Load(commands.Cog, name="onLoad"):
    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        await insert_guild(guild)

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild):
        remove_guild(guild.id)


def setup(client):
    global discord_cli
    discord_cli = client
    client.add_cog(_Load(client))
