import os, discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_BETA_TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents)
bot.load_extension("cogs.events")
bot.load_extension("cogs.ban-purger")
bot.load_extension("cogs.deletos")
bot.load_extension("cogs.deleters")
bot.load_extension("cogs.purging_stick")
bot.load_extension("cogs.user_nuke")
bot.load_extension("cogs.shield")
bot.load_extension("cogs.filter")

bot.run(TOKEN)