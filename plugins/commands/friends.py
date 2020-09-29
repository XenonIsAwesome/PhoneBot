from disco.bot import Plugin
from tinydb import TinyDB, Query
from util.embedder import friendlist_embed
from util.misc import wip

class Friends(Plugin):
    @Plugin.command('friendlist')
    def on_friendlist_command(self, event):
        with TinyDB('phonebot.json') as db:
            try:
                friendlist = db.search(Query().guild_id == event.guild.id)[0]['friendlist']
            except Exception as e:
                event.msg.reply("You don\'t have any friends yet loser...")
                return
        event.msg.reply('', embed=friendlist_embed(friendlist, event.guild))
    
    @Plugin.command('add', '<snowflake:int> [name:str...]')
    def on_add_command(self, event, snowflake, name=None):
        if not name: name = snowflake
        wip(event)
        pass

