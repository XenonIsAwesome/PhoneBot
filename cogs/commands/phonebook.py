from discord.ext import commands
from util.embedder import friendlist_embed
from util.db_management.db_connection import connect_to_db

db = connect_to_db()


class _Phonebook(commands.Cog, name="Phonebook related commands"):
    @commands.command(name='phonebook', aliases=['fl', 'friendlist', 'pb'])
    async def _phonebook(self, ctx):
        fl = db.find_one({'guild_id': ctx.guild.id})['friendlist']
        if not fl:
            return await ctx.send("You don\'t have any friends yet loser...")
        await ctx.send('', embed=friendlist_embed(fl, ctx.guild))

    @commands.command(name='add')
    async def _add(self, ctx, snowflake, name=None):
        if not name:
            name = snowflake

        fl = db.find_one({'guild_id': ctx.guild.id})['friendlist']
        if db.find_one({'guild_id': int(snowflake)}):
            fl[name] = int(snowflake)
            db.update_one({'guild_id': ctx.guild.id}, {"$set": {'friendlist': fl}})
            await ctx.send(f'Added {snowflake} to your phonebook as {name}.')
        else:
            await ctx.send('I don\'t know that server...')

    @commands.command(name='remove', aliases=['rm'])
    async def _remove(self, ctx, friend):
        fl = db.find_one({'guild_id': ctx.guild.id})['friendlist']
        if not fl.get(friend):
            return await ctx.send(f"The server isn\'t on your friendlist...")

        fl.pop(friend)  # more common than del idk if its better
        # del fl[friend]
        db.update_one({'guild_id': ctx.guild.id}, {"$set": {'friendlist': fl}})

        await ctx.send(f"Removed {friend} from your phonebook.")


def setup(client):
    client.add_cog(_Phonebook(client))
