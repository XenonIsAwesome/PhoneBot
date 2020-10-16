from disco.bot import Plugin
from tinydb import TinyDB, Query
from util.embedder import friendlist_embed
from util.misc import wip

class Friends(Plugin):
    @Plugin.command('friendlist')
    def on_friendlist_command(self, event):
        with TinyDB('phonebot.json') as db:
            try:
                friendlist = db.get(Query().guild_id == event.guild.id)['friendlist']
            except Exception as e:
                event.msg.reply("You don\'t have any friends yet loser...")
                return
        event.msg.reply('', embed=friendlist_embed(friendlist, event.guild))
    
    @Plugin.command('add', '<snowflake:int> [name:str...]')
    def on_add_command(self, event, snowflake, name=None):
        if not name: name = snowflake
        
        with TinyDB('phonebot.json') as db:
            fl = db.get(Query().guild_id == event.guild.id)['friendlist']
            if db.get(Query().guild_id == snowflake):
                fl[name] = snowflake
                db.update({'friendlist': fl}, Query().guild_id == event.guild.id)
            else:
                event.msg.reply('I don\'t know that server...')
    

    @Plugin.command('remove', '<friend:str...>')
    def on_remove_command(self, event, friend):
        try:
            snowflake = db.get(Query().guild_id == event.guild.id)['friendlist'][friend]
        except Exception as e:
            event.msg.reply(f"The server isn\'t on your friendlist...")
            return
        
        with TinyDB('phonebot.json') as db:
            fl = db.get(Query().guild_id == event.guild.id)['friendlist']
            del fl[friend]
            db.update({'friendlist': fl}, Query().guild_id == event.guild.id)

