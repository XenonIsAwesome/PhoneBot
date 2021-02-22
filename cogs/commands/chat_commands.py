from discord.ext import commands

from util.datatypes.conversations import *
from util.db_management.db_connection import connect_to_db

db = connect_to_db()
discord_cli = None


class _ChatCommands(commands.Cog, name='Conversations commands'):
    @commands.command(name='text')
    async def on_text_command(self, ctx, *members):
        if ctx.guild in (member for member in (conv.members for conv in CONVERSATIONS)):
            return await ctx.send("You\'re already in a conversation...")

        members_objects = [ctx.guild]
        fl = db.find_one({'guild_id': ctx.guild.id})['friendlist']

        for member in members:
            if member not in fl.keys():
                return await ctx.send(f"You\'re not friends with the server {member}...")

            guild = discord_cli.get_guild(fl[member])
            members_objects.append(guild)

        invite = Invite(members_objects, ctx.guild, TextConv)
        await invite.send_accept(ctx)
        await ctx.send("Sent the invite!")

    @commands.command(name='voice')
    async def on_voice_command(self, ctx, members):
        return

    @commands.command(name='disconnect')
    async def on_disconnect_command(self, ctx):
        CONVERSATIONS.pop(ctx.guild.id).members.pop(ctx.guild.id)
        await ctx.send("Disconnected from the conversation.")


def setup(client):
    global discord_cli
    discord_cli = client
    client.add_cog(_ChatCommands(client))