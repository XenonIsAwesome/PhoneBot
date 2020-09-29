from util.embedder import text_message_embed
from tinydb import TinyDB, Query


class Conversation:
    def __init__(self, members):
        self.members = members


class TextConversation(Conversation):
    def send(self, event, source_channel):
        embed = text_message_embed(event, event.content)

        for member in [member for member in self.members if not source_channel]:
            with TinyDB('phonebot.json') as db:
                mem_channel_id = db.search(Query().guild_id == member)[0]['text_channel_id']
            self.bot.client.state.guilds[int(member)].channels[mem_channel_id].send_message('', embed=embed)


class VoiceConversation(Conversation):
    pass
