__author__ = "tina-maiello@github"

import discord
from logging_formatter import LoggingFormatter

# top level bot client class which has generically usable functions, is a child of discord.Client
class BotClient(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.logger = LoggingFormatter.init_logger(__name__)


    # once bot mounts and connects
    async def on_ready(self):
        self.logger.info(f'connected: {self.user}')


    # attempt to find channel in cache, if not, then fetch it via the API
    async def get_channel_details(self,channel_id):
        channel = self.get_channel(channel_id)
        return channel or await self.fetch_channel(channel_id)



    ###
    # TODO: refactor get_message to have a singular entrypoint,
    # and handle the different message types inside
    ###
    

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


