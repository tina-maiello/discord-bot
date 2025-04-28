__author__ = "tina-maiello@github"


from bot.BotClient import BotClient
import discord
from logging_formatter import LoggingFormatter
from db import MongoWrapper


# class which is child of BotClient, which is a child of discord.client
class StarboardClient(BotClient):
    def __init__(self, intents: discord.Intents, emoji='⭐', starboard_channel="starboard", reaction_count=3):
        super().__init__(intents=intents)
        self.logger = LoggingFormatter.init_logger(__name__)
        self.emoji = emoji
        self.starboard_channel = starboard_channel
        self.reaction_count = reaction_count
        self.mongo_wrapper = MongoWrapper.MongoWrapper()

    # attempt to resolve the starboard channel for a given guild
    async def find_starboard_channel(self,guild_id): # TODO: refactor this to check a guilds table in db
        for guild in self.guilds:                    # if not there then resolve via this O(xn) approach
            if guild_id == guild.id:
                for channel in guild.channels:
                    if(channel.name == self.starboard_channel):
                        self.logger.debug(f'starboard channel found: {channel}')
                        return channel


    # checks if message already exists in starboard
    # TODO: refactor this to 
    async def is_message_unique(self, starboard_channel, starboard_message):
        if starboard_message.channel.name == self.starboard_channel: # was starboarding things in starboard channel
            return False                                             # need a better way to fix this than this
        elif starboard_message.reference: # removing starboarding a forwarded message for now
            return False                  # because it caused strange behavior in the discord client
        async for message in starboard_channel.history(limit=250):
            if message.reference:
                details = await self.get_message_details_via_reference(message.reference)
                if details.jump_url == starboard_message.jump_url:
                    return False
        return True


    # attempt to send message in starboard
    async def send_in_starboard(self,starboard_channel,starboard_message):
        if starboard_channel is not None:
            message_unique = await self.is_message_unique(starboard_channel,starboard_message)

            if message_unique:
                await starboard_message.forward(starboard_channel)
                details = await self.get_message_details_via_id(starboard_message)
                temp_dict = {"message_id":str(details.id)}
                self.mongo_wrapper.insert_into_starboard_messages(temp_dict)
                self.logger.debug(f'sent message in starboard')
        else:
            self.logger.error(f'failed to find starboard channel in Guild: {starboard_message.guild.name},{starboard_message.guild.id}')


    # fires every single time there is a reaction in the server
    async def on_raw_reaction_add(self,payload):
        self.logger.debug(f'reaction added: {payload}')

        if payload.emoji.name == self.emoji:
            # fetch details about the message
            message = await self.get_message_details_via_payload(payload)

            for reaction in message.reactions:
                if reaction.count >= int(self.reaction_count) and reaction.emoji == self.emoji:
                    self.logger.debug(f'>={self.reaction_count} {self.emoji} reactions on message: {message}')

                    # fetch details about the guild's starboard channel
                    starboard_channel = await self.find_starboard_channel(message.guild.id)

                    await self.send_in_starboard(starboard_channel,message)


    # fires every single time there is a reaction removed in the server
    async def on_raw_reaction_remove(self,payload):
        self.logger.debug(f'reaction removed: user: {payload}')

        if payload.emoji.name == self.emoji:
            message = await self.get_message_details_via_payload(payload)

            for reaction in message.reactions:
                if reaction.count < self.reaction_count and reaction.emoji == self.emoji:
                    self.logger.info(f'number of {self.emoji} reactions fell below {self.reaction_count}! removing message from starboard?')
                    # might not actually remove from starboard for now i am unsure
