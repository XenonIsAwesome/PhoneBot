from util.embedder import text_message_embed, accept_message_embed
from tinydb import TinyDB, Query

CONVERSATIONS = []
INVITES = []


class Conversation:
    def __init__(self, members):
        self.members = []
        for member in members:
            with TinyDB('phonebot.json') as db:
                if not db.get(Query().guild_id == member): return
                    member = self.bot.client.state.guilds[member_snowflake]
            self.members.append(member)
    
    def add_member(self, member_snowflake):
        with TinyDB('phonebot.json') as db:
            if not db.get(Query().guild_id == member): return
        member = self.bot.client.state.guilds[member_snowflake]
        self.members.append(member)


class ConversationInvite(Conversation):
    def __init__(self, members, conv_type):
        self.conv_type = conv_type
        self.messages = []
        super().__init__(members)

    def send_accept(self, event, invite_initiator):
        for member in [int(m) for m in self.members]:
            if not db.get(Query().guild_id == snowflake):
                event.msg.reply("I don\'t know one of the servers...")
                return
        
        embed = accept_message_embed(event, members)

        for member in [member for member in self.members if member.id != invite_initiator.id]:
            with TinyDB('phonebot.json') as db:
                mem_channel_id = db.get(Query().guild_id == member)['text_channel_id']
            msg = member.channels[mem_channel_id].send_message('', embed=embed)
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
