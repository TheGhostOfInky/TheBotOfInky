import nextcord
from nextcord.ext import commands


class emojilister(commands.Cog):
    """
    This category's purpose is to get the emojis from the current server
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_emoji")
    async def get_emoji(self, ctx: commands.Context):
        """
        This command gets all emojis in a server in their displayed form
        """
        msgstr = getMsgstr(ctx, 2000)
        for i in msgstr:
            await ctx.send(i)

    @commands.command(name="get_emoji_txt")
    async def get_emoji_txt(self, ctx: commands.Context):
        """
        This command gets all emojis in a server in their raw text form
        """
        msgstr = getMsgstr(ctx, 1998)
        for i in msgstr:
            await ctx.send("`{}`".format(i))


def getMsgstr(ctx: commands.Context, lim: int) -> list[str]:
    if not ctx.guild:
        raise Exception("Invalid guild")

    emoji_str: list[str] = [str(emoji) for emoji in ctx.guild.emojis]
    msg_str: list[str] = [""]
    index: int = 0

    for emoji in emoji_str:
        if (len(msg_str[index]) + len(emoji)) < lim:
            msg_str[index] += emoji
        else:
            index += 1
            msg_str.append(emoji)

    return msg_str


def setup(bot):
    bot.add_cog(emojilister(bot))
