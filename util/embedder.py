from discord import Embed
from datetime import datetime as dt
from random import choice


def text_message_embed(message):
    embed = Embed(
        title=message.content,
        color=choice([0x209CF6, 0x8172D7])#,
        #timestamp=dt.utcnow().isoformat()
    )

    embed.set_author(
        name=message.author,
        url=f"""https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}""",
        icon_url=message.author.avatar_url
    )

    embed.set_footer(text=f"From {message.guild.name}")
    return embed


def accept_message_embed(ctx, members):
    embed = Embed(
        title="""
React with :white_check_mark: to accept.
React with :x: to ignore.
        """,
        color=0xfefefe
    )

    embed.set_author(
        name=f'{ctx.message.guild.name} wants to start a text conversation with this server.',
        icon_url=ctx.message.guild.icon_url
    )

    embed.add_field(
        name='Members:',
        value=', '.join([mem.name for mem_id, mem in members.items()]),
        inline=False
    )

    return embed


def welcome_message_embed(guild):
    embed = Embed(
        title='Thanks for using 𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩',
        color=0x2ECC71
    )

    embed.set_author(
        name=guild.name,
        icon_url=guild.icon_url
    )

    return embed


def friendlist_embed(friendlist, guild):
    embed = Embed()

    embed.set_author(
        name=guild.name,
        icon_url=guild.icon_url
    )

    friends_field = '\n'.join(
        [f'**{name}: {snowflake}**' for name, snowflake in friendlist.items()]
    )

    embed.add_field(
        name='Friends:',
        value=friends_field,
        inline=False
    )

    return embed
