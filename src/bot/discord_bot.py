__author__ = "tina-maiello@github"

import os
from dotenv import load_dotenv
import discord
import logging

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


# client = discord.Client(intents=intents)
class BotClient(discord.Client):
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
        return await channel.fetch_message(payload.message_id)


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


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())
    logger.addHandler(console_handler)
    load_dotenv('data/.env')
    intents = discord.Intents.default()
    intents.message_content = True
    bot_secret = os.environ.get("BOT_SECRET")
    client = BotClient(intents=intents, logger=logger)
    client.run(bot_secret)


if __name__ == "__main__":
    main()