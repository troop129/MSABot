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

class generalCommands(commands.Cog, name='General Server Commands'):
  '''These are the commands for general servers'''

  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx):
    infile = open('storage/blacklist','rb')
    self.banned = pickle.load(infile)
    infile.close()
    for id in self.banned:
      if int(format(ctx.author.id)) == id:
        return False
    return True

  @commands.command(name = 'reverse', aliases = ['uno', 'nou', 'no u'])
  async def reverse(self, ctx):
    cards = ['https://i.imgur.com/IxDEdxW.png', 'https://i.imgur.com/3WDcYbV.png']
    await ctx.reply(random.choice(cards)) 

  @commands.command(name = 'github', aliases = ['git', 'source'])
  async def github(self, ctx):
    await ctx.reply('Check out my source code: https://github.com/troop129/AbidBot')

def setup(bot):
	bot.add_cog(generalCommands(bot))