from disco.bot import Plugin
from util.misc import to_unix_timestamp, wip


class GeneralCommands(Plugin):
    @Plugin.command('ping')
    def on_ping_command(self, event):
        reply = event.msg.reply(':ping_pong: Pinging ...')

        reply.edit(
            f':ping_pong: Pong!\n'
            f'Latency is {round(to_unix_timestamp(reply.timestamp) - to_unix_timestamp(event.msg.timestamp), 2)}ms'
        )

    @Plugin.command('help', '[command:str...]')
    def on_help_command(self, event):
        wip(event)
