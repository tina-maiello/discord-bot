# discord-bot

my personal discord bot

## running locally (i dont know why you would do this)
create a file named ".env" with a value
       
    BOT_SECRET="<your key here>"
    
(optional) create a venv (may be slightly different on your system)

    python3 -m venv .venv
    source .venv/bin/activate.fish

install & run

    pip3 install -r requirements.txt
    python3 discord_bot.py
