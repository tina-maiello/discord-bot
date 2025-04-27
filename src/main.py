from bot import StarboardClient
from logging_formatter import LoggingFormatter
from dotenv import load_dotenv
import discord
import argparse
from os import environ

# argument parsing
parser = argparse.ArgumentParser(description="discord bot")
parser.add_argument("-e","--emoji", help="takes in a custom unicode emoji to use as 'starboard' emoji",required=False)
parser.add_argument("-sc","--starboard_channel", help="takes in a custom string to set as starboard channel",required=False)
parser.add_argument("-rc","--reaction_count", help="takes in an integer number of reactions to put message into starboard_channel")

def main():
    logger = LoggingFormatter.init_logger(__name__)
    token_path = "data/.env"
    logger.debug(f'setting environment variables from: {token_path}')
    load_dotenv(token_path)
    intents = discord.Intents.default()
    intents.message_content = True
    token_name = "BOT_SECRET"
    logger.info(f'getting token from environment variable {token_name}')
    bot_secret = environ.get(token_name)
    args = parser.parse_args()
    if args.reaction_count:
        if args.emoji and args.channel:
            client = StarboardClient.StarboardClient(intents=intents,emoji=args.emoji,starboard_channel=args.channel, reaction_count=args.reaction_count)
        else:
            client = StarboardClient.StarboardClient(intents=intents, reaction_count=args.reaction_count)
    else:
        client = StarboardClient.StarboardClient(intents=intents)
    client.run(bot_secret)


if __name__ == "__main__":
    main()