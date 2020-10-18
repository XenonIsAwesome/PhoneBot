from disco.bot import Plugin
from util.misc import wip
from datatypes.conversations import *
from os import getenv


class Chat(Plugin):
    @Plugin.listen("MessageCreate")
    def on_message_create(self, event):
        if event.author.id == getenv("CLIENT_ID"):
            return
        if event.guild.id not in [
            member.id for members in [conv.members for conv in CONVERSATIONS]
        ]:
            return

        [
            conv.send(event, event.guild.id)
            for conv in CONVERSATIONS
            if event.guild.id in conv.members
        ]

    @Plugin.listen("MessageReactionAdd")
    def on_reaction_create(self, event):
        wip(event)
        pass