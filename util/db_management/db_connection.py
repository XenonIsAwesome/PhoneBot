from pymongo import MongoClient


def connect_to_db():
    mongo = MongoClient\
        ("mongodb+srv://PhoneBot:phonebot2021@cluster0.jiisa.mongodb.net/PhoneBotDB?retryWrites=true&w=majority")

    guild_db = mongo.PhoneBotDB.Guilds
    return guild_db


db = connect_to_db()
