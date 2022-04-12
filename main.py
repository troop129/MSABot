import os
from keep_alive import keep_alive
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
	command_prefix="!",
	case_insensitive=True,
  intents = intents
)

bot.author_id = 446835150685208576
bot.remove_command("help")

@bot.event 
async def on_ready(): 
  print("Logged in as " + str(bot.user))
  print("I'm in " + str(len(bot.guilds)) + " servers so far.")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='your every command (!help)'), status=discord.Status.do_not_disturb)
  
extensions = [
	'cogs.cog_developer',
  'cogs.cog_general',
  'cogs.cog_tictactoe',
  'cogs.cog_fun',
  'cogs.cog_help',
  'cogs.cog_islamic'
]

if __name__ == '__main__': 
	for extension in extensions:
		bot.load_extension(extension) 

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)