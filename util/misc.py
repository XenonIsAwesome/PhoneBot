from util.datatypes.conversations import *
import os
from discord import Client as bot


def to_unix_timestamp(discord_dt):
    return discord_dt.timestamp()


async def wip(ctx):
    await ctx.send('This command is still WIP...')


def has_admin_role(member, admin_roles):
    for mem_role in member.roles:
        for admin_role in admin_roles:
            if mem_role.id == admin_role:
                return True
    return False


def walk_cogs(cogs_dir):
    cogs = []
    wip = []
    for root, folders, files in os.walk(cogs_dir):
        for name in files:
            if (cog_name := os.path.join(root, name)).endswith('.py'):
                if name not in wip:
                    cogs.append(cog_name.replace('/', '.').replace('\\', '.').replace('.py', ''))
        for folder in folders:
            walk_cogs(folder)
    return cogs
