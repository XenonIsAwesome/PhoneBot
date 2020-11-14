from disco.bot.bot import BotConfig


def get_config():
    config = BotConfig()
    config.commands_require_mention = False
    config.commands_prefix = "phone."
    config.plugins = [
        "plugs.commands.friends",
        "plugs.commands.general",
        "plugs.commands.settings",
        "plugs.events.load"
    ]
    return config


def wip(event):
    event.msg.reply('This command is still WIP...')


def to_unix_timestamp(discord_dt):
    return discord_dt.timestamp()


def has_admin_role(event, admin_roles):
    for mem_role in event.guild.members[event.msg.author.id].roles:
        for admin_role in admin_roles:
            if mem_role.id == admin_role:
                return True
    return False
