from disco.types.message import MessageEmbed


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