from pymongo import MongoClient
from logging_formatter import LoggingFormatter
from os import environ

class MongoWrapper():
    def __init__(self):
        self.logger = LoggingFormatter.init_logger(__name__)
        self.client = MongoClient(environ.get('DB_SECRET'))


    def insert_into_starboard_messages(self, message_dict):
        db = self.client.starboard
        col = db['messages']
        self.logger.debug(f'{col}')
        result = col.insert_one(message_dict)
        self.logger.debug(f'{result}')