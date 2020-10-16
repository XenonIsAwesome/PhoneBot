from disco.bot import Plugin
from tinydb import TinyDB, Query, where
from util.embedder import welcome_message_embed
from disco.types.channel import ChannelType

class Setup(Plugin):
    @Plugin.listen('GuildCreate')
    def on_guild_create(self, event):
        with TinyDB('phonebot.json') as db:
            if db.get(Query().guild_id == event.guild.id): return

            # Inserting the guild into the database                
            db.insert(
                {
                    'guild_id': event.guild.id,
                    'admin_roles': [],
                    'text_channel_id': '',
                    'voice_channel_id': '',
                    'friendlist': {}
                }
            )

            # Sending the welcome message
            for chan in list(event.guild.channels.values())
                if chan.type == ChannelType.GUILD_TEXT:
                    chan.send_message('', embed=welcome_message_embed(event.guild))

    @Plugin.listen('GuildDelete')
    def on_guild_create(self, event):
        with TinyDB('phonebot.json') as db:
            # Removing the guild from the database                
            db.remove(where('guild_id') == event.guild.id)
    
            
