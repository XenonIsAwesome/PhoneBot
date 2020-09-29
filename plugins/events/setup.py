from disco.bot import Plugin
from tinydb import TinyDB, Query, where


class Setup(Plugin):
    @Plugin.listen('GuildCreate')
    def on_guild_create(self, event):
        with TinyDB('phonebot.json') as db:
            if len(db.search(Query().guild_id == event.guild.id)) == 0:
                db.remove(where('guild_id') == event.guild.id)
            db.insert(
                {
                    'guild_id': event.guild.id,
                    'welcome': True,
                    'everyone': False,
                    'admin_roles': [],
                    'prefix': 'phone.',
                    'text_channel_id': '',
                    'voice_channel_id': '',
                    'friendlist': {}
                }
            )
