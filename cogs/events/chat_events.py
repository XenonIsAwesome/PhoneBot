from discord.ext import commands

from util.misc import has_admin_role
from util.datatypes.conversations import *
from util.db_management.db_connection import connect_to_db

from os import getenv

db = connect_to_db()
discord_cli = None


async def delete_reaction(payload):
    channel = discord_cli.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    return await message.reactions[-1].remove()


class _ChatEvents(commands.Cog):
    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if str(message.author.id) == getenv("CLIENT_ID"):
            return
        conv = CONVERSATIONS.get(message.guild.id)
        if not conv:
            return
        if message.content.startswith(db.find_one({'guild_id': message.guild.id})['prefix']):
            return
        if message.channel.id == db.find_one({'guild_id': message.guild.id})['text_channel_id']:
            await conv.send(message, message.guild.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.member.id) == getenv("CLIENT_ID"): return
        invite = INVITES.get(payload.guild_id)
        if not invite: return
        if payload.emoji.name not in '✅❌':
            return await delete_reaction(payload)
        admin_roles = db.find_one({'guild_id': payload.guild_id})['admin_roles']
        if admin_roles and not has_admin_role(payload.member, admin_roles):
            return await delete_reaction(payload)
        if payload.emoji.name == '❌':
            return await delete_reaction(payload)

        if invite.conv_type == TextConv:
            conv = CONVERSATIONS.get(invite.initiator.id)
            if conv:
                guild = discord_cli.get_guild(payload.guild_id)
                conv.add_member(guild)
                CONVERSATIONS[payload.guild_id] = conv
            else:
                guild = discord_cli.get_guild(payload.guild_id)
                CONVERSATIONS[payload.guild_id] = TextConv([guild, invite.initiator])
                CONVERSATIONS[invite.initiator.id] = CONVERSATIONS[payload.guild_id]
        else: return


def setup(client):
    global discord_cli
    discord_cli = client
    client.add_cog(_ChatEvents(client))