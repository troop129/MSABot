import asyncio
import discord
import discord.ext
from discord.ext import commands
import pickle

class helpCommands(commands.Cog, name='Help Server Commands'):
  '''These are the help commands for general servers'''
  
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name= 'help', invoke_without_command=True)
  async def help(self, ctx):
    embed = discord.Embed(title="MSA Bot Help Menu", colour=discord.Colour(0x1), description="Use the commands below to explore the many MSA Bot commands.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    embed.add_field(name="Fun", value="`!help fun <#>`", inline=True)
    embed.add_field(name="Utility", value="`!help utility <#>`", inline=True)
    embed.add_field(name="Islamic", value='`!help islamic`')
    embed.set_footer(text='The help menu is stil being rewritten at this time. Thank you for your patience.')
    await ctx.send(embed=embed)

  @help.command(name="fun")
  async def fun(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="MSA Bot Fun Commands", colour=discord.Colour(0x1), description="MSA Bot loves to have fun.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!joke", value="Random (possibly dad) joke.", inline=inl)
      embed.add_field(name="!emojify <message>", value="Convert your text into text-emoji-things.", inline=inl)
      embed.add_field(name="!avatar <mention>*", value="Get a user's avatar. Leave out mention to get your own.", inline=inl)
      embed.add_field(name="!clap <message>", value="Puts clap emojis between your words. For extra emphasis, you know?", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
      embed.add_field(name="!inspire", value="Get a random inspirational quote.", inline=inl)
      embed.add_field(name="!f", value="Can I get an F in the chat?", inline=inl)
      embed.add_field(name="!echo <channel>* <message>", value="Echoes your message in the channel of your choice. Leave out channel paramter for echo in same channel.", inline=inl)
      embed.add_field(name="!sarcasm <phrase>", value="tHiS CoMmAnD iS tHe BeSt!", inline=inl)
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {}!'.format(arg))
    else:
      await ctx.send(embed=embed)
  
  @help.command(name="utility")
  async def utility(self, ctx, arg:int = 1):
    inl = False
    pages = 2
    embed = discord.Embed(title="MSA Bot Utility Commands", colour=discord.Colour(0x1), description="MSA Bot can be very helpful to you.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if arg == 0 or arg == 1:
      embed.add_field(name="!choose <c1> | <c2>", value='Seperate choices with a "|" please.', inline=inl)
      embed.add_field(name="!countdown <time> <name>*", value="Countdown for seconds or minutes, ex: 30s, 5m. Add optional timer name after for organization.", inline=inl)
      embed.add_field(name="!vote <question>", value="Brings up a vote...", inline=inl)
      embed.add_field(name="!poll <p1> | <p2>", value="Starts a poll, can have up to 9 options.", inline=inl)
      embed.add_field(name="!search <parameter>", value="Search bing for whatever term you like (writing a google api atm).", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    elif arg == 2:
      embed.add_field(name="!define <word>", value="Returns the Oxford Dictionary's definition of a word.", inline=inl)
      embed.add_field(name="!coinflip", value="Flip a coin!", inline=inl)
      embed.add_field(name="!8ball", value="It's an 8ball.", inline=inl)
      embed.add_field(name="!randomnumber <#> <#>", value="Returns a random integer between the two value parameters (inclusive).", inline=inl)
      embed.set_footer(text='Page 2 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {}!'.format(arg))
    else:
      await ctx.send(embed=embed)

  @help.command(name='islamic', aliases=['islam'])
  async def islamic(self, ctx, arg:int = 1):
    inl = False
    pages = 1
    embed = discord.Embed(title="MSA Bot Islamic Commands", colour=discord.Colour(0x1), description="Asalamu Alaykum")
    if arg == 0 or arg == 1:
      embed.add_field(name="!prayertimes <MM/DD/YYYY>*", value="Lists the prayer times for the date, leave out to get todays.", inline=inl)
      embed.add_field(name="!pt <prayer>", value="See when a specific prayer or event (iftaar/suhoor) is.", inline=inl)
      embed.add_field(name="!setlocation <city>", value="Change your location for the prayer time calculation", inline=inl)
      embed.set_footer(text='Page 1 of {}. A "*" means optional. Leave out the "<>".'.format(pages))
    if arg > pages or arg < 1:
      await ctx.send('There is no page {}!'.format(arg))
    else:
      await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(helpCommands(bot)) 