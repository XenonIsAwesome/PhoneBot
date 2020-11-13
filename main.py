from dotenv import load_dotenv
from pathlib import Path
from os import system, getenv

load_dotenv(Path('.env'))

print(f"Invite: https://discord.com/api/oauth2/authorize?client_id={getenv('CLIENT_ID')}&permissions=0&scope=bot")
system(f'py -m disco.cli --config config.json --token {getenv("TOKEN")}')
