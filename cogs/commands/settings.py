from discord.ext import commands
from discord import Forbidden
from util.db_management.db_connection import connect_to_db

db = connect_to_db()


class _Settings(commands.Cog, name="Settings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup')
    async def _setup(self, ctx):
        admin_roles = ctx.message.role_mentions

        # making the unique category and channels for phonebot to use
        try:
            category = await ctx.guild.create_category(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩')
            tchannel = await category.create_text_channel(
                name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩-conversation')
            vchannel = await category.create_voice_channel(
                name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩 Conversation')

            # adding all the values to the database
            db.update_one({'guild_id': ctx.guild.id}, {"$set": {
                    'text_channel_id': tchannel.id,
                    'voice_channel_id': vchannel.id
            }})

            if admin_roles:
                db.update(
                    {'guild_id': ctx.guild.id},
                    {"$set": {'admin_roles': [role.id for role in admin_roles]}},
                )
        except Forbidden as e:
            ctx.send(
                f'I dont have enough premissions to do that...\n**`Error: {e.args[0]}`**'
            )

    @commands.command(name='prefix')
    async def _prefix(self, ctx, prefix):
        db.update_one(
            {'guild_id', ctx.guild.id},
            {"$set": {'prefix': prefix}}
        )


def setup(client):
    client.add_cog(_Settings(client))
