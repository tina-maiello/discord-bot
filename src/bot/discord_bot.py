__author__ = "tina-maiello@github"


import os
from dotenv import load_dotenv
import discord
import logging
from logging_formatter import LoggingFormatter
import starboard
import argparse


# argument parsing
parser = argparse.ArgumentParser(description="discord bot")
parser.add_argument("-e","--emoji", help="takes in a custom unicode emoji to use as 'starboard' emoji",required=False)
parser.add_argument("-sc","--starboard_channel", help="takes in a custom string to set as starboard channel",required=False)
parser.add_argument("-rc","--reaction_count", help="takes in an integer number of reactions to put message into starboard_channel")


# top level bot client class which had generically usable functions, is a child of discord.Client
class BotClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.logger = LoggingFormatter.init_logger("discord_bot")


    # once bot mounts and connects
    async def on_ready(self):
        self.logger.info(f'connected: {self.user}')


    # attempt to find channel in cache, if not, then fetch it via the API
    async def get_channel_details(self,channel_id):
        channel = self.get_channel(channel_id)
        return channel or await self.fetch_channel(channel_id)


    # find message via API call, only way to get message.reactions
    async def get_message_details_via_payload(self,payload):
        channel = await self.get_channel_details(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        self.logger.debug(f'message found!: {message}')
        return message
    

    # find message via API call, only way to get message.reactions
    async def get_message_details_via_id(self,message):
        channel = await self.get_channel_details(message.channel.id)
        message_details = await channel.fetch_message(message.id)
        self.logger.debug(f'message found!: {message_details}')
        return message_details
    

    # find message via API call, only way to get message.reactions
    async def get_message_details_via_reference(self,reference):
        channel = await self.get_channel_details(reference.channel_id)
        message_details = await channel.fetch_message(reference.message_id)
        self.logger.debug(f'message found!: {message_details}')
        return message_details


def main():
    logger = LoggingFormatter.init_logger(__name__)
    token_path = "data/.env"
    logger.debug(f'setting environment variables from: {token_path}')
    load_dotenv(token_path)
    intents = discord.Intents.default()
    intents.message_content = True
    token_name = "BOT_SECRET"
    logger.info(f'getting token from environment variable {token_name}')
    bot_secret = os.environ.get(token_name)
    args = parser.parse_args()
    if args.reaction_count:
        if args.emoji and args.channel:
            client = starboard.Starboard(intents=intents,emoji=args.emoji,starboard_channel=args.channel, reaction_count=args.reaction_count)
        else:
            client = starboard.Starboard(intents=intents, reaction_count=args.reaction_count)
    else:
        client = starboard.Starboard(intents=intents)
    client.run(bot_secret)


if __name__ == "__main__":
    main()