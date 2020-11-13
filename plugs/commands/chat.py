from disco.bot import Plugin
from util.misc import wip
from datatypes.conversations import *
from tinydb import TinyDB, Query


class Chat(Plugin):
    @Plugin.command('text', '<members:str...>')
    def on_text_command(self, event, members):
        if event.guild in [member for member in [conv.members for conv in CONVERSATIONS]]:
            event.msg.reply("You\'re already in a conversation...")
            return

        member_snowflakes = []
        with TinyDB('phonebot.json') as db:
            for member in members.split(' '):
                if member not in db.get(Query().guild_id == int(event.guild.id))['friendlist'].keys():
                    event.msg.reply("You are not friends with this server...")
                    return

                snowflake = db.get(Query().guild_id == int(event.guild.id))['friendlist'][member]
                member_snowflakes.append(snowflake)

        invite = ConversationInvite(member_snowflakes, TextConversation)
        invite.send_accept(event, event.guild)

    @Plugin.command('voice', '<members:str...>')
    def on_voice_command(self, event, members):
        members = members.split(' ')
        wip(event)
        pass