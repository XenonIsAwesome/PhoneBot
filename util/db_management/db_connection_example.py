# rename this file to db_connection.py

from pymongo import MongoClient


def connect_to_db():
    mongo = MongoClient("add-your-mongo-uri")

    guild_db = mongo.PhoneBotDB.Guilds
    return guild_db


db = connect_to_db()
