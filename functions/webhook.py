import settings
from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_PYTHON_LOGS = settings.WEBHOOK_PYTHON_LOGS

async def exec_logs(err_cmd, command):

    webhook_status = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, username="Python")
    embed = DiscordEmbed(title='Report', description='Logs do Python', color='93b6ed')
    embed.add_embed_field(name='Erros de Execução do Comando', value=err_cmd)
    embed.add_embed_field(name='Comando Utilizado', value=command)
    embed.set_timestamp()
    webhook_status.add_embed(embed)
    webhook_status.execute()


async def python_logs(message):
    # Discord to send logs to Python Logs Channel of the bot
    webhook_status = DiscordWebhook(url=WEBHOOK_PYTHON_LOGS, rate_limit_retry=True, username="Python")
    embed = DiscordEmbed(title='LiteSecBot', description=message, color='ff0000')
    embed.set_timestamp()
    webhook_status.add_embed(embed)
    webhook_status.execute()

