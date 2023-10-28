#############################################################
# Import dep and libs
import discord
import nextcord
import youtube_dl
import ffmpeg
import args
import yt_dlp as youtube_dl
import asyncio
from nextcord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import os, settings
from dotenv import load_dotenv
#############################################################
# Youtube DL Setup
youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
#############################################################

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, args, volume=0.5):
        super().__init__(args, source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegAudio(filename, **ffmpeg_options), data=data)

class Musica(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(name='join', help='Chama o bot para a sala.')
    async def join(self, ctx, *, channel: nextcord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(name='play', help='Inicia uma música.')
    async def play(self, ctx, *, query):
        source = nextcord.PCMVolumeTransformer(nextcord.FFmpegAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f"Erro:{e}") if e else None)

        await ctx.reply(f"Iniciando a música: {query}")

    @commands.command(name='yt', help='Inicia uma música.')
    async def yt(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Erro: {e}") if e else None
            )

            await ctx.reply(f"Iniciando a música: {player.title}")
            ctx.voice_client.play(
                player, after=lambda e: print(f"Erro: {e}") if e else None
            )
            
            await ctx.reply(f"Iniciando a música: {player.title}")

    @commands.command()
    async def stream(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

    @commands.command(name='stop', help='Para a música.')
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.reply("Você não está conectado em um chat de voz")
                raise commands.CommandError("Usuário não está conectado em um chat de voz")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Musica(bot))
