from bot import StarboardClient
from logging_formatter import LoggingFormatter
from dotenv import load_dotenv
import discord
import argparse
from os import environ
logger = LoggingFormatter.init_logger(__name__)


# argument parsing
def get_args():
    parser = argparse.ArgumentParser(description="discord bot")
    parser.add_argument("-e","--emoji", help="takes in a custom unicode emoji to use as 'starboard' emoji",required=False)
    parser.add_argument("-sc","--starboard_channel", help="takes in a custom string to set as starboard channel",required=False)
    parser.add_argument("-rc","--reaction_count", help="takes in an integer number of reactions to put message into starboard_channel")
    return parser.parse_args()


def load_dotenv_environ_variables(path):
    logger.debug(f'setting environment variables from: {path}')
    load_dotenv(path)


def get_intents_for_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    return intents


def init_bot(token_name):
    intents = get_intents_for_discord_bot()
    args = get_args()
    if args.reaction_count:
        if args.emoji and args.channel:
            client = StarboardClient.StarboardClient(intents=intents,emoji=args.emoji,starboard_channel=args.channel, reaction_count=args.reaction_count)
        else:
            client = StarboardClient.StarboardClient(intents=intents, reaction_count=args.reaction_count)
    else:
        client = StarboardClient.StarboardClient(intents=intents)
    logger.info(f'getting token from environment variable {token_name}')
    client.run(environ.get(token_name))
    

def main():
    load_dotenv_environ_variables("data/.env")
    init_bot("BOT_SECRET")


if __name__ == "__main__":
    main()