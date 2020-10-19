from datatypes.conversations import INVITES, CONVERSATIONS


def wip(event):
    event.msg.reply('This command is still WIP...')


def get_conv(member_id, conv_type=None):
    convers = CONVERSATIONS
    if conv_type:
        convers = [conv for conv in CONVERSATIONS if type(conv) == conv_type]
    for conv in convers:
        if member_id in conv.members: return conv
    return None


def get_invite(message_id):
    for invite in INVITES:
        if message_id in invite.messages:
            return invite
    return None


def has_admin_role(event, admin_roles):
    for mem_role in event.guild.members[event.msg.author.id].roles:
        for admin_role in admin_roles:
            if mem_role.id == admin_role:
                return True
    return False
