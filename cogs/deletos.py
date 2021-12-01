import discord
from discord.ext import commands
class deletos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def deletos(self,ctx):
        if ctx.message.reference:
            message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            await message.delete()
        else:
            await ctx.send("No replies found")
def setup(bot):
    bot.add_cog(deletos(bot))