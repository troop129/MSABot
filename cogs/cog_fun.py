import requests
import json
import random
import asyncio
import discord
import aiohttp
import discord.ext
import typing
import pickle
from discord.ext import commands

class funCommands(commands.Cog, name='Fun Commands'):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name = 'joke')
  async def joke(self, ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    payload = response.json()
    await ctx.send(payload['setup'])  
    await asyncio.sleep(2)
    await ctx.send(payload['punchline'])

  @commands.command(name = 'emojify', aliases = ['e', 'emoji'])
  async def emojify(self, ctx, *, arg = None):
    if arg != None:
      converted = ''
      for l in arg:
        if l.isalpha():
          converted += ':regional_indicator_' + l.lower() +':' + ' '
        elif l == ' ':
          converted += '   '
        elif l == '?':
          converted += ':question: '
        elif l == '!':
          converted += ':exclamation: '
        else:
          converted += l + ' '
      await ctx.reply(converted)
    else:
      await ctx.reply('What do I emojify?')
  
  @commands.command(name = 'avatar', aliases = ['a', 'av'])
  async def avatar(self, ctx, member: discord.Member = None):
    author = ''
    choices = ['It better not be anime...', "It's an okay pfp...", 'I hate it.', 'Why not use my face instead?', ':sick:', ':eyes:', ':heart_eyes:', ':+1:', 'Need a new one?', "It's time to change..."]
    if member == None:
      author = ctx.author.name
      embed=discord.Embed(title= "Your Avatar", description=random.choice(choices))
      embed.set_image(url=ctx.author.avatar_url)
    elif self.bot.user.name == member.name:
      embed=discord.Embed(title= "Your Avatar", description='LOOK AT THAT BEAUTIFUL FACE OMG!')
      embed.set_image(url=member.avatar_url)
    else:
      author = member.name
      embed=discord.Embed(title= "{}'s Avatar".format(author), description=random.choice(choices))
      embed.set_image(url=member.avatar_url)
    await ctx.reply(embed=embed)

  @commands.command(name = 'clap')
  async def clap(self, ctx, *, arg = None):
    if arg is None:
      await ctx.reply('I guess I will clap to nothing then.')
    else:
      message = arg.replace(' ', ' :clap: ')
      message = ':clap: {} :clap:'.format(message)
      await ctx.reply(message)

  @commands.command(name = 'inspire', aliases = ['ins'])
  async def inspire(self, ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.reply(quote)

  @commands.command(name = 'f', aliases = ['rip'])
  async def f(self, ctx):
    cards = ['https://tenor.com/view/press-f-pay-respect-coffin-burial-gif-12855021']
    await ctx.reply(random.choice(cards))

  @commands.command(name = 'echo')
  async def echo(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, args = None):
    if args is None:
      await ctx.reply('What do I echo?')
    else: 
      if channel is None:
        await ctx.send(args)
      else:
        await channel.send(args)

  @commands.command(name = 'wonky', aliases = ['sarcastic', 'caps', 'sarcasm', 's'])
  async def wonky(self, ctx, *, args=None):
    if args == None:
      await ctx.reply('I gUeSs IlL mAkE fUn Of YoU iNsTeAd...')
    else:
      ret = ""
      i = True 
      for char in args:
        if i:
            ret += char.upper()
        else:
            ret += char.lower()
        if char != ' ':
            i = not i
      await ctx.send(ret)

def setup(bot):
	bot.add_cog(funCommands(bot))