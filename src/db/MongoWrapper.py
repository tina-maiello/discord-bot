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
        return result


    def insert_into_starboard_guilds(self, guild_dict):
        db = self.client.starboard
        col = db['guilds']
        self.logger.debug(f'{col}')
        result = col.insert_one(guild_dict)
        self.logger.debug(f'{result}')
        return result
    

    def find_guilds_starboard(self, guild_id):
        db = self.client.starboard
        col = db['guilds']
        self.logger.debug(f'{col}')
        result = col.find_one({"guild_id":guild_id})
        self.logger.debug(f'{result}')
        return result
    

    def find_starboard_message(self,message_id):
        db = self.client.starboard
        col = db['messages']
        self.logger.debug(f'{col}')
        result = col.find_one({"message_id":message_id})
        self.logger.debug(f'{result}')
        return result