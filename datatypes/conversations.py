from util.embedder import text_message_embed, accept_message_embed
from tinydb import TinyDB, Query
from disco.types.message import Emoji

conv_q = Query()


CONVERSATIONS = []
INVITES = []


class Conversation(object):
    def __init__(self, first_members):
        self.members = []
        for m in first_members:
            self.add_member(m)
    
    def add_member(self, member_snowflake):
        with TinyDB('C:\\Users\\ofek1\\Desktop\\Folders\\github-repos\\BOTTEST\\phonebot.json') as db:
            if not db.get(conv_q.guild_id == member_snowflake): return
        member = self.bot.client.state.guilds[member_snowflake]
        self.members.append(member)


class ConversationInvite(Conversation):
    def __init__(self, members, conv_type):
        self.conv_type = conv_type
        self.messages = []
        super(ConversationInvite, self).__init__(members)

    def send_accept(self, event, invite_initiator):
        for member in [m.id for m in self.members]:
            with TinyDB('C:\\Users\\ofek1\\Desktop\\Folders\\github-repos\\BOTTEST\\phonebot.json') as db:
                if not db.get(Query().guild_id == member.id):
                    return event.msg.reply("I don\'t know one of the servers...")

        embed = accept_message_embed(event, self.members)

        for member in [member for member in self.members if member.id != invite_initiator.id]:
            with TinyDB('C:\\Users\\ofek1\\Desktop\\Folders\\github-repos\\BOTTEST\\phonebot.json') as db:
                mem_channel_id = db.get(Query().guild_id == member)['text_channel_id']
            msg = member.channels[mem_channel_id].send_message('', embed=embed)
            msg.add_reaction(Emoji('✅'))
            msg.add_reaction(Emoji('❌'))
            
            self.messages.append(msg)
        
        INVITES.append(self)


class TextConversation(Conversation):
    def send(self, event, source_channel):
        embed = text_message_embed(event, event.content)

        for member in [member for member in self.members if member.id != source_channel]:
            with TinyDB('phonebot.json') as db:
                mem_channel_id = db.get(Query().guild_id == member)['text_channel_id']
            member.channels[mem_channel_id].send_message('', embed=embed)


class VoiceConversation(Conversation):
    pass
