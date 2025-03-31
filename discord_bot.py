__author__ = "tina-maiello@github"

import os
from dotenv import load_dotenv
load_dotenv()
bot_secret = os.environ.get("BOT_SECRET")


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(levelname)s  %(name)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)

import discord
# set the intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f'connected: {client.user}')


# attempt to find channel in cache, if not, then fetch it via the API
async def get_channel_details(channel_id):
    channel = client.get_channel(channel_id)
    return channel or await client.fetch_channel(channel_id)


# find message via API call, only way to get message.reactions
async def get_message_details(payload):
    channel = await get_channel_details(payload.channel_id)
    return await channel.fetch_message(payload.message_id)


# attempt to resolve the starboard channel for a given guild
async def find_starboard_channel(guild_id):
    for guild in client.guilds:
        if guild_id == guild.id:
            for channel in guild.channels:
                if(channel.name == 'starboard'):
                    logger.debug(f'starboard found: {channel}')
                    return channel


# fires every single time there is a reaction in the server
@client.event
async def on_raw_reaction_add(payload):
    logger.debug(f'reaction added: {payload}')

    if payload.emoji.name == '⭐':
        # fetch details about the message
        message = await get_message_details(payload)
        logger.debug(f'message found!: {message}')

        for reaction in message.reactions:
            if reaction.count >= 3 and reaction.emoji.name == '⭐':
                logger.debug(f'>=3 ⭐ reactions on message: {message}')

                # fetch details about the guild's starboard channel
                starboard_channel = await find_starboard_channel(message.guild.id)

                if starboard_channel is not None:
                    await starboard_channel.send(message.jump_url)
                else:
                    logger.error(f'failed to find starboard channel in Guild: {message.guild.name},{message.guild.id}')
            

# fires every single time there is a reaction removed in the server
@client.event
async def on_raw_reaction_remove(payload):
    logger.debug(f'reaction removed: user: {payload}')


client.run(bot_secret)