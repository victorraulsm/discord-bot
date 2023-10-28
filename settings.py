#############################################################
# Import dep and libs

import os
from dotenv import load_dotenv

load_dotenv()

# SETTINGS OF THE BOT.
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_PYTHON_LOGS = os.getenv('WEBHOOK_PYTHON_LOGS')
DESCRIPTION = "LiteSec Bot - Made by Raul Victor"
PREFIX = "$"
BOTSTATUS = "Spotify"
INTENTS_MEMBER = True
INTENTS_MESSAGE_CONTENT = True

# OPENAI API TOKEN
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')