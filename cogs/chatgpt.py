#############################################################
# Import dep and libs
import os, settings
import openai
import nextcord
import aiohttp
from dotenv import load_dotenv
from nextcord.ext import commands
from functions import webhook

class ChatGPT(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='chatgpt', help='Integração para utilizar o ChatGPT.')
    async def gpt(self, ctx, *, prompt: str, member: nextcord.Member = None):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 100,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,
            }
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_TOKEN}"}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    # Extract the response text from 'choices'
                    response_text = response[0]['choices'][0]['text']
                    embed = nextcord.Embed(title="Resposta do ChatGPT:", description=response_text)
                    await ctx.reply(embed=embed)
                else:
                    await ctx.reply("Erro: Falha ao obter resposta da API OpenAI.")

#            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
#                response = await resp.json()
#                embed = nextcord.Embed(title="Resposta do ChatGPT:", description=response)
#                await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(ChatGPT(bot))