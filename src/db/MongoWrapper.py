from pymongo import MongoClient
from logging_formatter import LoggingFormatter
from os import environ

class MongoWrapper():
    def __init__(self):
        self.logger = LoggingFormatter.init_logger(__name__)
        self.client = MongoClient(environ.get('DB_SECRET'))

    def get_mongo_client(self):
        return self.client


    db = client.starboard
    col = db['messages']
    print(db)

    test_dict = {"message_id":"123","message":"321"}

    x = col.insert_one(test_dict)