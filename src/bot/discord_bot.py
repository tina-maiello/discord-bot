__author__ = "tina-maiello@github"


import os
from dotenv import load_dotenv
import discord
import argparse
import logging
from LoggingFormatter import LoggingFormatter
import starboard


class BotClient(discord.Client):
    logger = LoggingFormatter.init_logger(__name__)
    
    def __init__(self, intents: discord.Intents, logger: logging.Logger):
        super().__init__(intents=intents)
        self.logger = logger
        print(self.logger.level)


    async def on_ready(self):
        self.logger.info(f'connected: {self.user}')


    # attempt to find channel in cache, if not, then fetch it via the API
    async def get_channel_details(self,channel_id):
        channel = self.get_channel(channel_id)
        return channel or await self.fetch_channel(channel_id)


    # find message via API call, only way to get message.reactions
    async def get_message_details(self,payload):
        channel = await self.get_channel_details(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        self.logger.debug(f'message found!: {message}')
        return message
    

def main():
    logger = LoggingFormatter.init_logger(__name__)
    load_dotenv('data/.env')
    intents = discord.Intents.default()
    intents.message_content = True
    bot_secret = os.environ.get("BOT_SECRET")
    client = starboard.Starboard(intents=intents, logger=logger)
    client.run(bot_secret)


if __name__ == "__main__":
    main()