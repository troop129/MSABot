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

  @commands.command(name = 'inspire', aliases = ['ins'])
  async def inspire(self, ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.reply(quote)

  @commands.command(name = 'joke')
  async def joke(self, ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    payload = response.json()
    await ctx.send(payload['setup'])  
    await asyncio.sleep(2)
    await ctx.send(payload['punchline'])

  @commands.command(name = '8ball', aliases = ['8'])
  async def eightball(self, ctx, *, arg: str = ''):
    if arg != '':
      q = arg
      response = requests.get('https://8ball.delegator.com/magic/JSON/' + q)
      data = json.loads(response.content)
      question = data['magic']['question']
      answer = data['magic']['answer']
      embed=discord.Embed(title="AbidBot - 8ball", description="The answers to all of your questions...")
      embed.set_thumbnail(url="https://i.imgur.com/1WRfu41.png")
      embed.add_field(name="Your Question", value=question, inline=False)
      embed.add_field(name="My Answer", value=answer, inline=False)
      embed.set_footer(text="I hope your query was answered.")
      await ctx.reply(embed=embed)
    elif arg == '':
      m = ctx.reply('I have an 8ball question for you instead...')
      await asyncio.sleep(2)
      await m.edit(m + "\nWhat are you asking me, you troglodyte?")

  @commands.command(name = 'choose')
  async def choose(self, ctx, *, arg = None):
    if arg == None:
      await ctx.send("What do I choose between, you foofer?")
    else:
      data = arg
      choices = []
      try:
        if '|' in data:
          choices = data.split('|')
          if 't' in choices and 'd' in choices and ctx.author.id == self.bot.author_id:
            final = 't'
          else:
            final = random.choice(choices)
          await ctx.send('I choose...')
          await asyncio.sleep(2)
          await ctx.send(final)
        else:
          await ctx.send('Separate choices with "|" please.')
      except:
        await ctx.send('I think you messed up. Try rephrasing.')

  @commands.command(name = 'poll')
  async def poll(self, ctx, *, arg = None):
    if arg == None:
      await ctx.send("You need things to poll with...")
    else:
      data = arg
      choices = []
      words = ''
      nums = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
      reactions = ['<:1:822202649658392627>', '<:2:822202649699942468>',
'<:3:822202649691815968>', '<:4:822202649649872926>', '<:5:822202649633357855>', '<:6:822202648958730240>', '<:7:822202649722093598>', '<:8:822202649603473468>', '<:9_:822202649650397214>']
      try:
        if '|' in data:
          while '|' in data:
            choices.insert(len(choices), data[: data.index('|')])
            data = data[data.index('|')+1:]
            while data[0] == " ":
              data = data[1:]
          choices.insert(len(choices), data)
          if len(choices) > 9:
            await ctx.send('You can only have up to 9 options...')
            return
          else:
            count = 0
            for d in choices:
              words += '{} = **{}**\n'.format(reactions[count],d)
              count += 1
            m = await ctx.send('**{}** has made a new poll: \n{words}'.format(ctx.author.display_name, words=words))
            for i in range(0, len(choices)):
              await m.add_reaction(reactions[i])
        else:
          await ctx.send('Separate choices with "|" please.')
      except:
        await ctx.send('I think you messed up. Try rephrasing.')

  @commands.command(name = 'vote')
  async def vote(self, ctx, *, arg = None):
    if arg == None:
      await ctx.send('What do we vote on? Me?')
    else:
      if "?" not in arg:
        arg += "?"
      m = await ctx.send('**{} asks: ** {arg}'.format(ctx.author.display_name, arg=arg))
      await m.add_reaction('a:thumbs_up:812905599242862612')
      await m.add_reaction('a:thumbs_down:812905599103664159')

  @commands.command(name = 'countdown')
  async def countdown(self, ctx, *args):
    try:
      arg = args[0]
      letter = arg[-1]
      name = ' - '
      embed=discord.Embed(title="AbidBot Timer")
      try:
        catcher = args[1]
        for x in args:
          if args.index(x) != 0:
            name = name + x + ' '
      except:
        name = '' 

      if letter == 's':
        timeleft = int(arg[:-1])
        units = "** seconds left."
      elif letter == 'm':
        timeleft = int(arg[:-1])*60
        units = "** minutes left."
      
      embed.add_field(name="Timer started!" + name, value="You have **" + arg[:-1] + units, inline=False)
      m = await ctx.send(embed=embed)

      while timeleft > 90:
        await asyncio.sleep(60)
        timeleft -= 60
        embed=discord.Embed(title="AbidBot Timer")
        mins = ''
        if timeleft % 60 == 0:
          mins = str(int(timeleft/60))
          embed.add_field(name="Timer started!" + name, value="You have **" + mins + "** minutes left.", inline=False)
        else:
          embed.add_field(name="Timer started!" + name, value="You have **" + str(timeleft/60) + "** minutes left.", inline=False)
        await m.edit(embed=embed)
        
      while timeleft <= 90 and timeleft > 30:
        await asyncio.sleep(15)
        timeleft -= 15
        embed=discord.Embed(title="AbidBot Timer")
        embed.add_field(name="Timer started!" + name, value="You have **" + str(timeleft) + "** seconds left.", inline=False)
        await m.edit(embed=embed)
        
      while timeleft <= 30 and timeleft > 10:
        await asyncio.sleep(5)
        timeleft -= 5
        embed=discord.Embed(title="AbidBot Timer")
        embed.add_field(name="Timer started!" + name, value="You have **" + str(timeleft) + "** seconds left.", inline=False)
        await m.edit(embed=embed)
        
      while timeleft <= 10 and timeleft > 1:
        await asyncio.sleep(1)
        timeleft -= 1
        embed=discord.Embed(title="AbidBot Timer")
        embed.add_field(name="Timer started!" + name, value="You have **" + str(timeleft) + "** seconds left.", inline=False)
        await m.edit(embed=embed)

      if timeleft == 1:
        await asyncio.sleep(1)
        timeleft -= 1
        embed=discord.Embed(title="AbidBot Timer")
        embed.add_field(name="Timer ended!" + name, value="You have **0** seconds left!", inline=False)
        await m.edit(embed=embed)

    except:
      await ctx.send("Format time correctly please.")
      await asyncio.sleep(2)
      await ctx.send("Fool.")

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
      await ctx.send(converted)
    else:
      await ctx.send('What do I make into an emoji? You? Ok.')
      await asyncio.sleep(2)
      await ctx.send('<:smallbrain:813895629565984768>')

  @commands.command(name = 'reverse', aliases = ['uno', 'nou', 'no u'])
  async def reverse(self, ctx):
    cards = ['https://i.imgur.com/IxDEdxW.png', 'https://i.imgur.com/3WDcYbV.png']
    await ctx.send(random.choice(cards))
    
  @commands.command(name = 'f', aliases = ['rip'])
  async def f(self, ctx):
    cards = ['https://tenor.com/view/press-f-pay-respect-coffin-burial-gif-12855021']
    await ctx.send(random.choice(cards))

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
    await ctx.send(embed=embed)
  
  @commands.command(name = 'define', aliases = ['dictionary', 'definition'])
  async def define(self, ctx, arg:str = ''):
    if arg == '':
      await ctx.send('Since you failed to give me a word to define, I will get one myself.')
      await asyncio.sleep(2)
      await ctx.send('**{}**: A nincompoop who fails to use a bot properly.'.format((ctx.author.display_name).capitalize()))
    else:
      app_id = 'e762a89e'
      app_key = '47f395f230ba589e1f5874e4a68e27fa'
      language = 'en-us'
      word_id = arg
      url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word_id.lower()
      r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
      if r.status_code == 404:
        await ctx.send('Oops, **{}** is not a real word. Try checking your spelling.'.format(arg.capitalize()))
      elif r.status_code == 200:
        data = json.loads(r.content)
        embed=discord.Embed(title= "Definition of: {}".format((data['id'].capitalize())), description="An AbidBot dictionary call queried by: **{}**.".format(ctx.author.display_name))
        try:
          embed.add_field(name = 'Definition', value = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0].capitalize() , inline=False)
          try:
            embed.add_field(name = 'Example Sentence', value = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text'].capitalize() , inline=False)
          except:
            embed.add_field(name = 'Example Sentence', value = 'None given.' , inline=False)
          await ctx.send(embed=embed)
        except:
          pass
      else:
        await ctx.send('The API seems to have failed for some reason. Please try again.')
    
  @commands.command(name = 'clap')
  async def clap(self, ctx, *, arg = None):
    if arg is None:
      await ctx.send('I guess I will clap to nothing then.')
    else:
      message = arg.replace(' ', ' :clap: ')
      message = ':clap: {} :clap:'.format(message)
      await ctx.send(message)
  
  @commands.command(name = 'coinflip', aliases = ['hrt', 'headsortails', 'coin'])
  async def coinflip(self, ctx):
    choice = random.randint(1, 3)
    await ctx.send('Flipping a coin...')
    await asyncio.sleep(1.5)
    coin = ''
    if choice == 1:
      coin = 'tails'
    if choice == 2:
      coin = 'heads'
    await ctx.send('I choose **{}**.'.format(coin))
  
  @commands.command(name = 'numberchoose', aliases = ['randomint', 'randomnumber'])
  async def numberchoose(self, ctx, *, args = None):
    if args is not None:
      nums = args.split(' ')
      if len(nums) <= 1:
        await ctx.send("I can't choose with just one number...")
      else:
        try:
          least = int(nums[0])
          most = int(nums[1])
          if least > most:
            least, most = most, least
          elif least == most:
            await ctx.send("I choose...")
            await asyncio.sleep(2)
            await ctx.send('**{}**! Did you expect something else?'.format(least))
          else:
            number = random.randint(least,most)
            await ctx.send('Choosing a random number between **{}** and **{}**...'.format(least, most))
            await asyncio.sleep(2)
            await ctx.send('I choose **{}**!'.format(number))
        except ValueError:
          await ctx.send('I cannot choose you do not give numbers...')
    else:
      await ctx.send('In order to pick between numbers, I need numbers.')
      await asyncio.sleep(2)
      await ctx.send('*GiMmIe ThE nUmBeRs MaN!*')

  @commands.command(name = 'echo')
  async def echo(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, args = None):
    if args is None:
      await ctx.send('What do I echo?')
    else: 
      if channel is None:
        await ctx.send(args)
      else:
        await channel.send(args)

  @commands.command(name = 'search', aliases = ['bing', 'google'])
  async def search(self, ctx, *, args=None):
    if args is None:
      await ctx.send('What do I look up?')
    else:
      url = "https://bing-web-search1.p.rapidapi.com/search"
      querystring = {"q":args,"mkt":"en-us","textFormat":"Raw","safeSearch":"Off","freshness":"Day"}
      headers = {
          'x-bingapis-sdk': "true",
          'x-rapidapi-key': "1097c6051cmsh08616dcf75d9528p131eb8jsn141b3329d1e2",
          'x-rapidapi-host': "bing-web-search1.p.rapidapi.com"
          }
      response = requests.request("GET", url, headers=headers, params=querystring)
      data = json.loads(response.content)
      
      try:
        url = data['webPages']['webSearchUrl'] #search url
        matches = data['webPages']['totalEstimatedMatches'] # number of matches
        embed=discord.Embed(title= "Bing results for: {}".format((args.capitalize())), description="I found **{}** matches.".format(matches), url = url)

        for x in range(0,4):
          link = data['webPages']['value'][x]['url']
          urltitle = data['webPages']['value'][x]['name']
          snippet = data['webPages']['value'][x]['snippet']
          embed.add_field(name = '{}: {}'.format(x+1, urltitle), value = '{} [Link]({})'.format(snippet, link), inline = False)
      
        await ctx.send(embed=embed)
      except:
        await ctx.send('Oops, I could not find any results for that word :/')

  @commands.command(name = 'wonky', aliases = ['sarcastic', 'caps', 'sarcasm', 's'])
  async def wonky(self, ctx, *, args=None):
    if args == None:
      await ctx.send('I gUeSs IlL mAkE fUn Of YoU iNsTeAd...')
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

  @commands.command(name = 'github', aliases = ['git', 'source'])
  async def github(self, ctx):
    await ctx.send('Check out my source code: https://github.com/troop129/AbidBot')

def setup(bot):
	bot.add_cog(generalCommands(bot)) 