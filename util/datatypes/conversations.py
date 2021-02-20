from hashlib import sha256
from util.db_connection import connect_to_db
from discord.ext.commands import Bot as bot
from util.embedder import *

db = connect_to_db()

CONVERSATIONS = {}
INVITES = {}


def get_snowflakes_hash(item_snowflakes):  # useless
    return sha256(''.join(sorted(item_snowflakes))).hexdigest()


class Conversation(object):
    def __init__(self, first_members):
        self.members = {}
        [self.add_member(m) for m in first_members]

    def add_member(self, member):
        if not db.find_one({'guild_id': member.id}):
            return

        self.members[member.id] = member


class Invite(Conversation):
    def __init__(self, members, initiator, conv_type):
        self.initiator = initiator
        self.conv_type = conv_type
        self.messages = {}
        super(Invite, self).__init__(members)

    async def send_accept(self, ctx):
        global db

        for mem_id, member in self.members.items():
            if not db.find_one({'guild_id': mem_id}):
                return ctx.send(f"I don\'t know the server {member.name}...")
        embed = accept_message_embed(ctx, self.members)

        for mem_id, member in self.members.items():
            if mem_id != self.initiator.id:
                mem_channel_id = ""
                if self.conv_type == TextConv:
                    mem_channel_id = db.find_one({'guild_id': mem_id})['text_channel_id']
                #elif self.conv_type == VoiceConv:
                    #mem_channel_id = db.find_one({'guild_id': member})['voice_channel_id']

                msg = await member.get_channel(mem_channel_id).send('', embed=embed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')

                self.messages[msg.id] = msg

            for m_id, _ in self.members.items():
                INVITES[m_id] = self
            # invite_hash = get_snowflakes_hash((m.id for m in self.members))
            # INVITES[invite_hash] = self


class TextConv(Conversation):
    async def send(self, message, source):
        embed = text_message_embed(message)

        for m_id, m in self.members.items():
            if m_id != source:
                mem_channel_id = db.find_one({'guild_id': m_id})['text_channel_id']
                await m.get_channel(mem_channel_id).send('', embed=embed)


class VoiceConv(Conversation):
    pass
