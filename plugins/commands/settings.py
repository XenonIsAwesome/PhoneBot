from disco.bot import Plugin
from disco.api.http import APIException
from tinydb import TinyDB, Query, where


class SettingsCommands(Plugin):
    @Plugin.command('setup', '[admin_roles:str...]')
    def on_setup_command(self, event, admin_roles=None):
        if admin_roles:
            admin_roles = admin_roles.replace('<@', '').replace('>', '').split(' ')

        for role in admin_roles:
            if role not in event.guild.roles.keys:
                event.msg.reply('One of the roles doesn\'t exist in this guild...')
                return

        # making the unique category and channels for phonebot to use
        try:
            category_id = event.guild.create_category(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩').id
            tchannel = event.guild.create_text_channel(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩-conversation', parent_id=category_id).id
            vchannel = event.guild.create_voice_channel(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩 Conversation', parent_id=category_id).id

            # adding all the values to the database
            with TinyDB('phonebot.json') as db:
                db.update(
                    {
                        'text_channel_id': tchannel.id, 
                        'voice_channel_id': vchannel.id
                    },
                    Query().guild_id == event.guild.id
                )

                if admin_roles:
                    db.update(
                        {
                            'admin_roles': admin_roles
                        },
                        Query().guild_id == event.guild.id
                    )
        except APIException as e:
            event.msg.reply(f'I dont have enough premissions to do that...\n**`Error: {e.args[0]}`**')
