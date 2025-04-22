from discord_bot import BotClient
import discord
import logging
from LoggingFormatter import LoggingFormatter

class Starboard(BotClient):
    logger = LoggingFormatter.init_logger(__name__)

    def __init__(self, intents: discord.Intents, logger: logging.Logger):
        super().__init__(intents=intents, logger=self.logger)
        self.logger = logger
        print(self.logger.level)

    # attempt to resolve the starboard channel for a given guild
    async def find_starboard_channel(self,guild_id):
        for guild in self.guilds:
            if guild_id == guild.id:
                for channel in guild.channels:
                    if(channel.name == 'starboard'):
                        self.logger.debug(f'starboard found: {channel}')
                        return channel


    # fires every single time there is a reaction in the server
    async def on_raw_reaction_add(self,payload):
        self.logger.debug(f'reaction added: {payload}')

        if payload.emoji.name == '⭐':
            # fetch details about the message
            message = await self.get_message_details(payload)
            self.logger.debug(f'message found!: {message}')

            for reaction in message.reactions:
                if reaction.count >= 3 and reaction.emoji.name == '⭐':
                    self.logger.debug(f'>=3 ⭐ reactions on message: {message}')

                    # fetch details about the guild's starboard channel
                    starboard_channel = await self.find_starboard_channel(message.guild.id)

                    if starboard_channel is not None:
                        await starboard_channel.send(message.jump_url)
                    else:
                        self.logger.error(f'failed to find starboard channel in Guild: {message.guild.name},{message.guild.id}')
            

    # fires every single time there is a reaction removed in the server
    async def on_raw_reaction_remove(self,payload):
        self.logger.debug(f'reaction removed: user: {payload}')

        if payload.emoji.name == '⭐':
            message = await self.get_message_details(payload)

            for reaction in message.reactions:
                if reaction.count < 3 and reaction.emoji.name == '⭐':
                    self.logger.debug(f'')