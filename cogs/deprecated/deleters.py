import nextcord, re
from nextcord.ext import commands
from datetime import datetime, timedelta
regex = r"ni(.)\1{1,}er|niggr|\bni..er(\b|s\b)|fag\b|\bfag|(f|p)hag|\b(p|f)hg\b|(p|f)ahg|fags\b|fa(g)\1{1,}|(f|fa|fi|fh|ph|pha)(g)\1{1,}|thrann(y|ie)|tr(ha|ah)nn(y|ie)|trahnn(y|ie)|trann|trany|tranie|tr(o)\1{1,}(n|m)|k(i|1|l)ke|nigress|\bnegro|shitskin|chink|g(o)\1{1,}k|sodomite|‎|​|‏"


class deleters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clean_old")
    @commands.has_permissions(manage_messages=True)
    async def clean_old(self, ctx, channel: nextcord.TextChannel = None, time: int = 365):
        if channel:
            await search(ctx, channel, time, True)
        else:
            await ctx.send("No channel was specified")

    @commands.command(name="clean_new")
    @commands.has_permissions(manage_messages=True)
    async def clean_new(self, ctx, channel: nextcord.TextChannel = None, time: int = 365):
        if channel:
            await search(ctx, channel, time, False)
        else:
            await ctx.send("No channel was specified")

    @commands.command(name="clean_embed")
    @commands.has_permissions(manage_messages=True)
    async def clean_embed(self, ctx, channel: nextcord.TextChannel = None):
        if channel:
            print(f"Starting the purge of #{channel.name}")
            await ctx.send(f"Starting the purge of <#{channel.id}>")
            async for message in channel.history(limit=None, oldest_first=False):
                for embed in message.embeds:
                    if embed == "Empty":
                        return
                    string = ""
                    string += str(embed.description)
                    string += str(embed.author.name)
                    for field in embed.fields:
                        string += str(field)
                    string += str(embed.title)
                    if re.search(regex, string, re.IGNORECASE):
                        try:
                            await message.delete()
                        except:
                            await ctx.send(f"Unable to delete message {message.id}")
            await ctx.send("Channel embeds cleaned")
        else:
            await ctx.send("No channel was specified")

    # Error handling

    @clean_old.error
    async def clean_old_error(error, ctx, message):
        await ctx.send(message)

    @clean_new.error
    async def clean_new_error(error, ctx, message):
        await ctx.send(message)

    @clean_embed.error
    async def clean_embed_error(error, ctx, message):
        await ctx.send(message)


async def search(ctx, channel, time, oldest):
    d = datetime.today() - timedelta(days=time)
    print("OK")
    print(f"Starting the purge of the last {time} days in #{channel.name}")
    await ctx.send(f"Starting the purge of the last {time} days in <#{channel.id}>")
    count = 0
    igcount = 0
    loop = 0
    async for message in channel.history(limit=None, after=d, oldest_first=oldest):
        loop += 1
        if loop == 1000:
            print(f"#{channel.name} Del:{str(count)} Ig:{str(igcount)}")
            loop = 0
        if re.search(regex, message.content, re.IGNORECASE):
            await message.delete()
            count += 1
        else:
            igcount += 1
    print(
        f"Purged {str(count)} messages from #{channel.name}, ignored {str(igcount)} messages")
    await ctx.send(f"Purged {str(count)} messages from <#{channel.id}>, ignored {str(igcount)} messages")


def setup(bot):
    bot.add_cog(deleters(bot))
