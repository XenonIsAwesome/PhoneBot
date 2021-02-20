from pymongo import MongoClient
from os import getenv


def connect_to_db():
    mongo = MongoClient(getenv("MONGO"))

    guild_db = mongo.PhoneBotDB.Guilds
    return guild_db

db = connect_to_db()
