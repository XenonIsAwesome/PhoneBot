from util.db_management.db_connection import connect_to_db
from discord import TextChannel
from util.embedder import welcome_message_embed

db = connect_to_db()


async def sync_with_db(client):
    # getting guild info
    client_guilds = client.guilds
    db_guilds = []
    for document in db.find():
        if not document.get('statistics'):
            db_guilds.append(document)

    # adding desynced guild objects to the database
    for guild in client_guilds:
        if not db.find_one({'guild_id': guild.id}):
            await insert_guild(guild)

    # removing desynced guild document from the database
    for guild in db_guilds:
        if not client.get_guild(guild['guild_id']):
            remove_guild(guild['guild_id'])


async def insert_guild(guild):
    current_guild_amount = db.find_one({'statistics': True})['guild_amount']
    current_guild_amount += 1

    db.update_one({'statistics': True}, {"$set": {'guild_amount': current_guild_amount}})

    # Inserting the guild into the database
    db.insert_one({
        "guild_name": guild.name,
        "guild_id": guild.id,
        "admin_roles": [],
        "text_channel_id": "",
        "voice_channel_id": "",
        "friendlist": {},
        "prefix": 'phone.'
    })

    # Sending the welcome message
    for chan in guild.channels:
        if isinstance(chan, TextChannel):
            try: return await chan.send('', embed=welcome_message_embed(guild))
            except: continue


def remove_guild(guild_id):
    current_guild_amount = db.find_one({'statistics': True})['guild_amount']
    current_guild_amount -= 1

    db.update_one({'statistics': True}, {"$set": {'guild_amount': current_guild_amount}})

    db.delete_one({'guild_id': guild_id})
