#############################################################
# Import dep and libs

import os, settings, nextcord
import logging
import openai
from nextcord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

# Show the INFO level of logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

WEBHOOK_PYTHON_LOGS = settings.WEBHOOK_PYTHON_LOGS

#############################################################
description = settings.DESCRIPTION
intents = nextcord.Intents.default()
intents.members = settings.INTENTS_MEMBER
intents.message_content = settings.INTENTS_MESSAGE_CONTENT
activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=settings.BOTSTATUS)
status = nextcord.Status.online
#############################################################
# OpenAI
openai.api_key = settings.OPENAI_API_TOKEN
#############################################################
# Bot prefix 
bot = commands.Bot(command_prefix=settings.PREFIX, activity=activity, status=status, description=description, intents=intents)
#############################################################

# BOT INIT & STATUS
async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            cog = f"cogs.{file[:-3]}"
            try:
                logger.info(f"load_cogs: Trying Load Extension {cog}.")
                await load_webhook("loading", cog)

                bot.load_extension(cog)

                logger.info(f"load_cogs: Extension {cog} Loaded with sucess.")
                await load_webhook("loaded", cog)

            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)

                # Send a webhook if cog failed
                logger.error("load_cogs: Extension cogs.{} failed in load process. \n{}".format(cog, exc))
                await failed_webhook(cog, exc)


async def init_webhook():
    # Discord to send status of the bot
    webhook_status = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, username="Python")
    embed = DiscordEmbed(title='DiscordBot', description=f'{bot.user} se conectou com o Discord! (ID: {bot.user.id})', color='93b6ed')
    embed.set_timestamp()
    webhook_status.add_embed(embed)
    webhook_status.execute()


async def load_webhook(status, cog):
    if status == "loading":
        # Send the status of what cog is will load
        loading_webhook_cog = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, content=f"Trying Load Extension {cog}.")
        loading_webhook_cog.execute()      
    elif status == "loaded": 
        # Send the status of loading of cog
        loaded_webhook_cog = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, content=f"Extension {cog} Loaded with sucess.")
        loaded_webhook_cog.execute()


async def failed_webhook(cog, exc):
    # Send if cog failed
    failed_webhook_cog = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, content="Extension cogs.{} failed in load process. \n{}".format(cog, exc))
    failed_webhook_cog.execute()

        
@bot.event
async def on_ready():
    # Hello World
    logger.info(f'{bot.user} se conectou com o Discord! (ID: {bot.user.id})')

    # Discord to send status of the bot
    await init_webhook()

    # Load Cogs
    await load_cogs()


## Bot Commands end here!
bot.run(settings.TOKEN)
##############################################################

