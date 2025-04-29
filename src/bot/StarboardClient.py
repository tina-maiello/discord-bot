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
    async def find_starboard_channel(self,guild_id):
        db_channel = self.mongo_wrapper.find_guilds_starboard(guild_id)
        if db_channel:
            channel = await self.get_channel_details(db_channel['channel_id'])
            self.logger.debug(f'starboard channel found via db: {channel}')
            return channel
        for guild in self.guilds:
            if guild_id == guild.id:
                for channel in guild.channels:
                    if(channel.name == self.starboard_channel):
                        self.logger.debug(f'starboard channel found by iterating through guilds: {channel}')
                        self.mongo_wrapper.insert_into_starboard_guilds({"guild_id":guild.id,"channel_name":channel.name,"channel_id":channel.id})
                        return channel


    # checks if message already exists in starboard
    async def is_message_unique(self, starboard_channel, starboard_message):
        if starboard_message.channel.name == self.starboard_channel: # was starboarding things in starboard channel
            return False                                             # need a better way to fix this than this
        elif starboard_message.reference: # removing starboarding a forwarded message for now
            return False                  # because it caused strange behavior in the discord client
        
        # async for message in starboard_channel.history(limit=250):
        #     if message.reference:
        #         details = await self.get_message_details(message.reference)
        #         if details.jump_url == starboard_message.jump_url:
        #             return False
        if self.mongo_wrapper.find_starboard_message(starboard_message.id) is not None:
            self.logger.debug(f'message is already starboarded. message_id: {starboard_message.id}')
            return False
        return True
    
    # converts discord.Message object into a db valid insertable dictionary
    def convert_message_to_db_object(self,message):
        for reaction in message.reactions:
            if reaction.emoji == self.emoji:
                return {"message_id":message.id,"channel_id":message.channel.id,"guild_id":message.guild.id,"reaction_emoji":str(reaction.emoji),"reaction_count":reaction.count}


    # attempt to send message in starboard
    async def send_in_starboard(self,starboard_channel,starboard_message):
        if starboard_channel is not None:
            message_unique = await self.is_message_unique(starboard_channel,starboard_message)

            if message_unique:
                await starboard_message.forward(starboard_channel)
                details = await self.get_message_details(starboard_message)
                if self.mongo_wrapper.find_starboard_message(details.id) is None:
                    self.mongo_wrapper.insert_into_starboard_messages(self.convert_message_to_db_object(details))
                self.logger.info(f'sent message_id: {details.id} in starboard')
        else:
            self.logger.error(f'failed to find starboard channel in Guild: {starboard_message.guild.name},{starboard_message.guild.id}')


    # fires every single time there is a reaction in the server
    async def on_raw_reaction_add(self,payload):
        self.logger.debug(f'reaction added: {payload}')

        if payload.emoji.name == self.emoji:
            # fetch details about the message
            message = await self.get_message_details(payload)

            for reaction in message.reactions:
                if reaction.count >= int(self.reaction_count) and reaction.emoji == self.emoji:
                    self.logger.info(f'>={self.reaction_count} {self.emoji} reactions on message id: {message.id}')

                    # fetch details about the guild's starboard channel
                    starboard_channel = await self.find_starboard_channel(message.guild.id)

                    await self.send_in_starboard(starboard_channel,message)


    # fires every single time there is a reaction removed in the server
    async def on_raw_reaction_remove(self,payload):
        self.logger.debug(f'reaction removed: {payload}')

        if payload.emoji.name == self.emoji:
            message = await self.get_message_details(payload)

            for reaction in message.reactions:
                if reaction.count < self.reaction_count and reaction.emoji == self.emoji:
                    self.logger.info(f'number of {self.emoji} reactions fell below {self.reaction_count}! removing message from starboard?')
                    # might not actually remove from starboard for now i am unsure
