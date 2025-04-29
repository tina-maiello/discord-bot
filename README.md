# discord-bot

my personal discord bot

## running locally (i dont know why you would do this)
create a file named ".env" in the 'data' (./data/.env) folder with a value
       
    BOT_SECRET="<your key here>"

(optional) create a venv (may be slightly different on your system)

    python3 -m venv .venv
    source .venv/bin/activate.fish

install & run

    pip3 install -r requirements.txt
    python3 src/bot/discord_bot.py

## bugs
- attachments dupe checking doesnt work
    - doesnt really handle attachments at all right now
- explicitly handle reference of references
- more robustly consider if the message.id is also starboarded in a certain guild, could be starboarded in 2 guilds