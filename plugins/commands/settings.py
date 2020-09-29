from disco.bot import Plugin
from disco.api.http import APIException
from tinydb import TinyDB, Query, where


class SettingsCommands(Plugin):
    @Plugin.command('setup', '[admin_roles:str...]')
    def on_setup_command(self, event, admin_roles=None):
        if admin_roles:
            admin_roles = admin_roles.split(' ')

        # making the unique category and channels for phonebot to use
        try:
            category_id = event.guild.create_category(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩').id
            tchannel = event.guild.create_text_channel(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩-conversation', parent_id=category_id)
            vchannel = event.guild.create_voice_channel(name='𝙋𝙝𝙤𝙣𝙚𝘽𝙤𝙩 Conversation', parent_id=category_id)
        except APIException as e:
            event.msg.reply(f'I dont have enough premissions to do that.\n**`Error: {e.args[0]}`**')
            return

        # adding all the values to the database
