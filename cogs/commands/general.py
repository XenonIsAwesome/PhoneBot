from discord.ext import commands
from util.misc import to_unix_timestamp


class _General(commands.Cog, name="General commands"):
    @commands.command(name="ping", aliases=["latency"])
    async def _ping(self, ctx):
        msg = await ctx.send(":ping_pong: Pinging ...")
        await msg.edit(
            content=f":ping_pong: Pong!\n"
            f"Latency is {round(to_unix_timestamp(msg.created_at) - to_unix_timestamp(ctx.message.created_at), 2)}ms"
        )

    @commands.command(name="afek", hidden=True)
    async def _afek(self, ctx):
        return await ctx.send("`https://www.youtube.com/watch?v=NUYvbT6vTPs`")




def setup(client):
    client.add_cog(_General(client))