from disco.bot import Plugin
from util.misc import get_conv, get_invite, has_admin_role, wip
from datatypes.conversations import *
from os import getenv


class ChatEvents(Plugin):
    @Plugin.listen("MessageCreate")
    def on_message_create(self, event):
        if event.author.id == getenv("CLIENT_ID"): return
        if event.guild.id not in [member.id for member in [conv.members for conv in CONVERSATIONS]]: return

        get_conv(event.guild.id, conv_type=TextConversation).send(event, event.guild.id)

    @Plugin.listen("MessageReactionAdd")
    def on_reaction_create(self, event):
        if event.user_id == getenv("CLIENT_ID"): return
        invite = get_invite(event.msg.id)
        if not invite: return
        if event.emoji.name not in ['white_check_mark', 'x']: return event.delete()
        with TinyDB('phonebot.json') as db:
            admin_roles = db.get(Query().guild_id == event.guild.id)['admin_roles']
        if not has_admin_role(event, admin_roles): return event.delete()
        if event.emoji.name == 'x': return event.msg.delete()
        
        conv = None
        if invite.conv_type is TextConversation:
            conv = get_conv(event.guild.id, conv_type=TextConversation)
            if conv: conv.add_member(event.guild.id)
            else: CONVERSATIONS.append(TextConversation(event.guild.id))
        elif invite.conv_type is VoiceConversation: wip(event)
