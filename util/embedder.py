from disco.types.message import MessageEmbed
from datetime import datetime as dt
from random import choice


def text_message_embed(event):
    embed = MessageEmbed()
    embed.title = event.msg.content
    embed.color = str(choice([0x209CF6, 0x8172D7]))

    embed.set_author(
        name=event.author,
        url=
        f"""https://discordapp.com/channels/{event.guild.id}/{event.channel_id}/{event.id}""",
        icon_url=event.author.get_avatar_url())

    embed.timestamp = dt.utcnow().isoformat()
    embed.set_footer(text=f"From {event.guild.name}")

    return embed


def accept_message_embed(event, members):
    embed = MessageEmbed()
    embed.title = """
React with :white_check_mark: to accept.
React with :x: to ignore. 
    """
    embed.color = str(0xFEFEFE)

    embed.set_author(
        name=
        f'{event.guild.name} wants to start a text conversation with this server.',
        icon_url=event.guild.get_icon_url())

    if len(members) > 2:
        embed.add_field(name='Members:',
                        value=f"{', '.join([mem.name for mem in members])}",
                        inline=False)
    return embed


def welcome_message_embed(guild):
    embed = MessageEmbed()
    embed.title = 'Thanks for using 𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩'
    embed.color = str(0x2ECC71)

    embed.set_author(name=guild.name, icon_url=guild.get_icon_url())

    return embed


def friendlist_embed(friendlist, guild):
    embed = MessageEmbed()

    embed.set_author(name=guild.name, icon_url=guild.get_icon_url())

    friends_field = '\n'.join(
        [f'**{name}: {snowflake}**' for name, snowflake in friendlist.items()])
    embed.add_field(name='Friends:', value=friends_field, inline=False)

    return embed