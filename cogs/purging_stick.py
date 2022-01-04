import discord
from discord.ext import commands
class purging_stick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="purging_stick")
    @commands.has_permissions(kick_members=True)
    async def purging_stick(self,ctx):
        for member in ctx.guild.members:
            if len(member.roles) < 2:
                print(member)
                await member.kick(reason="Bot raid")
    @purging_stick.error
    async def purging_stick_error(error,ctx,message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(purging_stick(bot))