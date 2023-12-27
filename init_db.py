import pymongo
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

client = pymongo.MongoClient(config.get("API", "mongo_server"))


def get_db(drop=False):
    dbname = "MZALIK_db_debt_bot"
    if drop:
        client.drop_database(dbname)

    db = client[dbname]

    return db

