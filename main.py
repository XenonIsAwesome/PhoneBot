from dotenv import load_dotenv
from pathlib import Path
from os import system, getenv
from util.misc import get_invite

load_dotenv(Path('.env'))

print("Invite:", get_invite(getenv("CLIENT_ID")))
system(f'python -m disco.cli --config config.json --token {getenv("TOKEN")}')
