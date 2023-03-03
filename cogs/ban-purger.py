import nextcord, re
from nextcord.ext import commands
from base import nopings


class ban_purger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(ban_members=True)
    async def purge(self, ctx: commands.Context):
        """
        Purges all deleted banned accounts in the server's banlist.
        """
        if ctx.guild is None:
            raise Exception("Guild not found")

        bans = await ctx.guild.bans().flatten()
        banlist: list[str] = []

        pattern = re.compile(r"^Deleted User [\da-f]{8}$")

        for ban in bans:
            if pattern.match(ban.user.name):
                await ctx.guild.unban(user=ban.user, reason="Unbanned Disabled Account")
                banlist.append(str(ban.user))

        if banlist:
            if len(banlist) > 68:
                banlist = banlist[:68]
                banlist.append(f"(And {len(banlist) - 68} more)")

            banlog = "Unbanned the following disabled accounts:\n```\n" + \
                "\n".join(banlist) + "```"

            await ctx.reply(
                banlog,
                allowed_mentions=nopings
            )

        else:
            await ctx.reply(
                "There are no acccounts to purge",
                allowed_mentions=nopings
            )


def setup(bot):
    bot.add_cog(ban_purger(bot))
