import discord, re
from discord.ext import commands
class ban_purger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="purge")
    @commands.has_permissions(ban_members=True)
    async def purge(self,ctx):
        bans = await ctx.guild.bans()
        banlist = []
        bancount = 0
        for ban in bans:
            if re.search(r"^Deleted User .{8}\b", ban.user.name):
                await ctx.guild.unban(user=ban.user, reason="Unbanned Disabled Account")
                banlist.append(f"{ban.user.name}#{ban.user.discriminator}")
                bancount += 1
        if bancount != 0:
            if bancount > 68:
                banlist = banlist[:68]
                banlist.append(f"(And {bancount - 68} more)")
            banlog = "Unbanned the following disabled accounts:\n```\n"
            for ban in banlist:
                banlog = banlog + ban + "\n"
            banlog = banlog + "```"
            await ctx.send(banlog)
        else:
            await ctx.send("There are no acccounts to purge")

    @purge.error
    async def purge_error(error,ctx,message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ban_purger(bot))