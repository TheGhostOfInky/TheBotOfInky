import discord, re
from discord.ext import commands
from datetime import datetime, timedelta
regex = r"nigger(|s)|niggr|\bni..er(\b|s\b)|nigress|\bnegro|shitskin|fag\b|\bfag|fags\b|fagg|(f|fa|ph|pha)ggot|trann|trany|tranie|troon|troome|kike|chink|gook|sodomite|‎|​"
class deleters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean_old(self, ctx, channel: discord.TextChannel=None, time: int=365):
        d = datetime.today() - timedelta(days=time)
        if channel:
            print(f"Starting the purge of the last {time} days in #{channel.name}")
            await ctx.send(f"Starting the purge of the last {time} days in <#{channel.id}>")
            count = 0
            igcount = 0
            loop = 0
            global total
            async for message in channel.history(limit=None,after=d,oldest_first=True):
                loop += 1
                if loop == 1000:
                    print(f"#{channel.name} Del:{str(count)} Ig:{str(igcount)}")
                    loop = 0
                if re.search(regex, message.content, re.IGNORECASE):
                    await message.delete()
                    count += 1
                else:
                    igcount += 1
            print(f"Purged {str(count)} messages from #{channel.name}, ignored {str(igcount)} messages")
            await ctx.send(f"Purged {str(count)} messages from <#{channel.id}>, ignored {str(igcount)} messages")
        else:
            await ctx.send("No channel was specified")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean_new(self, ctx, channel: discord.TextChannel=None, time: int=365):
        d = datetime.today() - timedelta(days=time)
        if channel:
            print(f"Starting the purge of the last {time} days in #{channel.name}")
            await ctx.send(f"Starting the purge of the last {time} days in <#{channel.id}>")
            count = 0
            igcount = 0
            loop = 0
            global total
            async for message in channel.history(limit=None,after=d,oldest_first=False):
                loop += 1
                if loop == 1000:
                    print(f"#{channel.name} Del:{str(count)} Ig:{str(igcount)}")
                    loop = 0
                if re.search(regex, message.content, re.IGNORECASE):
                    await message.delete()
                    count += 1
                else:
                    igcount += 1
            print(f"Purged {str(count)} messages from #{channel.name}, ignored {str(igcount)} messages")
            await ctx.send(f"Purged {str(count)} messages from <#{channel.id}>, ignored {str(igcount)} messages")
        else:
            await ctx.send("No channel was specified")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean_embed(self, ctx, channel: discord.TextChannel=None):
        if channel:
            print(f"Starting the purge of #{channel.name}")
            await ctx.send(f"Starting the purge of <#{channel.id}>")
            async for message in channel.history(limit=None,oldest_first=False):
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
                        await message.delete()
            print("job done")
        else:
            await ctx.send("No channel was specified")
def setup(bot):
    bot.add_cog(deleters(bot))