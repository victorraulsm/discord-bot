import nextcord
from nextcord.ext import commands
from functions import webhook


class Chat(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Bem-Vindo ao servidor Development {member.mention}!")

    @commands.command(name='ola', help='Diga olá para o bot.')
    async def hello(self, ctx, *, member: nextcord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.reply('Olá {} ❤️'.format(member))
            await ctx.reply('Tudo bem com você!?')
        else:
            await ctx.reply('Olá {}... 🤔'.format(member))
            await ctx.reply('Não me lembro de você...')
        self._last_member = member

    # Handles errors of clear command
    @hello.error
    async def hello_error(self, ctx, error):
        error_message: str = f'$hello error: {str(error)}'
        await ctx.reply(error_message)
        await webhook.send_logs(error_message)

    @commands.command(name='ping', help='Descubra o ping do bot.')
    async def ping(self, ctx):
        ping = self.bot.latency*1000
        await ctx.reply("Minha latência é {:.2f} ms!".format(ping))
        if ping <= 10:
            await ctx.reply("Conexão muito boa. 🚀")
        elif ping >= 11 and ping <= 35:
            await ctx.reply("Conexão estável. ⏩")
        elif ping >=36 and ping <= 50:
            await ctx.reply("Conexão um pouco lenta. 🥲")
        elif ping >= 80:
            await ctx.reply("Conexão muito lenta. 💤💤💤")

    # Handles errors of ping command
    @ping.error
    async def ping_error(self, ctx, error):
        error_message: str = f'$ping error: {str(error)}'
        await ctx.reply(error_message)
        await webhook.send_logs(error_message)

    @commands.has_any_role("Owner", "Admin", "Moderator")
    @commands.command(name='clear', help='Limpar chat.')
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit = 10000)

    # Handles errors of clear command
    @clear.error
    async def clear_error(self, ctx, error):
        error_message: str = f'$clear error: {str(error)}'
        await ctx.reply(error_message)
        await webhook.send_logs(error_message)

def setup(bot):
    bot.add_cog(Chat(bot))