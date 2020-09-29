from disco.bot import Plugin
from util.misc import wip

class Chat(Plugin):
    @Plugin.command('text', '<members:str...>')
    def on_text_command(self, event, members):
        members = members.split(' ')
        wip(event)
        pass

    @Plugin.command('voice', '<members:str...>')
    def on_voice_command(self, event, members):
        members = members.split(' ')
        wip(event)
        pass