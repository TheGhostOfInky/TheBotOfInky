import discord
from discord.ext import commands
from datetime import datetime, timedelta
class user_nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def user_nuke(self,ctx,userid: int=0,time: int=30):
        if userid == 0 or userid > 999999999999999999 or userid < 100000000000000000:
            await ctx.send("Invalid user inputted")
        else:
            d = datetime.today() - timedelta(days=time)
            for channel in ctx.guild.text_channels:
                await ctx.send(f"Starting the purge of the messages of {userid} in #{channel.name}")
                c_count = 0
                async for message in channel.history(limit=None,after=d,oldest_first=True):
                    if message.author.id == userid:
                        c_count += 1
                        await message.delete()
                await ctx.send(f"Purged {c_count} messages from #{channel.name}")
            await ctx.send("All messages purged")
                    

def setup(bot):
    bot.add_cog(user_nuke(bot))