import discord, datetime, time
from discord.ext import commands
class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.command(name="ping")
    async def ping(self,ctx):
        await ctx.send(f'My ping is {round(1000*self.bot.latency)} ms!')
    
    @commands.command(name="echo")
    @commands.has_permissions(manage_messages=True)
    async def echo(self,ctx, channel: discord.TextChannel=None, *args):
        str = ""
        for arg in args:
            str += " " + arg
        await channel.send(str)
        await ctx.message.add_reaction("🚀")

    @commands.command(name="roles")
    async def roles(self, ctx, *, member: discord.Member=None):
        if member == None:
            member = ctx.message.author
        totalroles = member.roles[1:]
        rolelist = "\n ".join(["<@&" + str(r.id) + ">" for r in totalroles[::-1]])
        emb2 = discord.Embed(
            title = f"Roles of {member.name}#{member.discriminator}:",
            type = "rich", 
            description = rolelist,
            color = 0x0000FE,
        )
        emb2.set_footer(
            text = f"{len(totalroles)} roles"
        )
        await ctx.send(embed=emb2)
    
    @commands.command(name="about")
    async def about(self, ctx):
        emb1 = discord.Embed(
            title = "About:",
            type = "rich", 
            description = "A bot created by TheGhostOfInky#9229 for a series of custom actions not supported by other bots, this bot is not a retail product and is therefore not available for use in servers other than the ones supervised by its owner.",
            color = 0x0000FE,
        )
        emb1.set_author(
            name = "TheGhostOfInky#9229" ,
            url = "https://github.com/TheGhostOfInky" ,
            icon_url = "https://cdn.discordapp.com/attachments/860367460854792193/860369517740818463/inky-bi-ghost.gif"
        )
        emb1.set_footer(
            text = "Built with discord.py",
            icon_url = "https://cdn.discordapp.com/attachments/860367460854792193/860368832497844244/discordpy.png"
        )
        emb1.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/860367460854792193/860367501698531328/TheBotOfInky.png"
        )
        emb1.add_field(
            name = "Github link",
            value = "https://github.com/TheGhostOfInky/TheBotOfInky",
            inline = True
        )
        emb1.add_field(
            name = "Uptime:",
            value = str(datetime.timedelta(seconds=int(round(time.time()-startTime)))),
            inline = True
        )
        await ctx.send(embed=emb1)

    #Error Handling
    @ping.error
    async def ping_error(error,ctx,message):
        await ctx.send(message)
    @echo.error
    async def echo_error(error,ctx,message):
        await ctx.send(message)
    @roles.error
    async def roles_error(error,ctx,message):
        await ctx.send(message)
    @about.error
    async def about_error(error,ctx,message):
        await ctx.send(message)


def setup(bot):
    bot.add_cog(utilities(bot))