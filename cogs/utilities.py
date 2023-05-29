import nextcord, datetime, time, subprocess, json, io, aiohttp, os
from nextcord.ext import commands
from typing import Optional
from base import nopings

TERMUX = os.getenv("TERMUX_VERSION")


class utilities(commands.Cog):
    """
    Assorted utilities
    """
    start_time: float

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.start_time = time.time()

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Returns the current ping from the bot to the discord servers
        """
        await ctx.reply(
            content=f"My ping is {round(1000*self.bot.latency)} ms!",
            allowed_mentions=nopings
        )

    @commands.command(name="echo")
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx: commands.Context, channel: Optional[nextcord.TextChannel] = None, *args):
        """
        Correct usage: ,echo <channel> <message>
        Sends a message to another channel
        """
        if channel is None:
            if not isinstance(ctx.channel, nextcord.TextChannel):
                raise Exception("Invalid channel")
            channel = ctx.channel

        arg_list = " ".join(args)
        await channel.send(arg_list)
        await ctx.message.add_reaction("🚀")

    @commands.command(name="roles")
    async def roles(self, ctx: commands.Context, *, member: Optional[nextcord.Member] = None):
        """
        Correct usage: ,roles <member>
        Lists all the roles of a given user
        """
        if not member:
            if not isinstance(ctx.author, nextcord.Member):
                raise Exception("Invalid caller")
            member = ctx.author

        totalroles = member.roles[1:]
        rolelist = "\n ".join(f"<@&{r.id}>" for r in totalroles[::-1])

        emb2 = nextcord.Embed(
            title=f"Roles of {member}:",
            type="rich",
            description=rolelist,
            color=0x0000FE,
        )
        emb2.set_footer(
            text=f"{len(totalroles)} roles"
        )
        await ctx.reply(
            embed=emb2,
            allowed_mentions=nopings
        )

    @commands.command(name="about")
    async def about(self, ctx):
        """
        Displays information about the bot
        """
        emb1 = nextcord.Embed(
            title="About:",
            type="rich",
            description="A bot created by TheGhostOfInky#2853 for a series of custom actions not supported by other bots, this bot is not a retail product and is therefore not available for use in servers other than the ones supervised by its owner.",
            color=0x0000FE,
        )
        emb1.set_author(
            name="TheGhostOfInky#2853",
            url="https://github.com/TheGhostOfInky",
            icon_url="https://cdn.discordapp.com/attachments/860367460854792193/860369517740818463/inky-bi-ghost.gif"
        )
        emb1.set_footer(
            text="Built with nextcord",
            icon_url="https://github.com/nextcord/nextcord/raw/master/assets/logo.png"
        )
        emb1.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/860367460854792193/860367501698531328/TheBotOfInky.png"
        )
        emb1.add_field(
            name="Github link",
            value="https://github.com/TheGhostOfInky/TheBotOfInky",
            inline=True
        )
        emb1.add_field(
            name="Uptime:",
            value=str(datetime.timedelta(
                seconds=round(time.time() - self.start_time))),
            inline=True
        )
        await ctx.reply(
            embed=emb1,
            allowed_mentions=nopings
        )

    @commands.command(name="profile")
    async def profile(self, ctx: commands.Context, user: Optional[nextcord.Member] = None):
        """
        Correct usage: ,profile <user>
        Displays the user's server profile picture
        """
        if not user:
            if not isinstance(ctx.author, nextcord.Member):
                raise Exception("Invalid caller")
            user = ctx.author

        emb: nextcord.Embed = nextcord.Embed(
            title=str(user),
            type="rich"
        )
        emb.set_image(url=user.display_avatar.url)
        await ctx.reply(
            embed=emb,
            allowed_mentions=nopings
        )

    @commands.command(name="banner")
    async def banner(self, ctx: commands.Context, usr: Optional[nextcord.Member] = None):
        """
        Correct usage: ,banner <user>
        Displays the user's banner image
        """
        if not usr:
            if not isinstance(ctx.author, nextcord.Member):
                raise Exception("Invalid caller")
            usr = ctx.author

        async with ctx.channel.typing():
            user = await self.bot.fetch_user(usr.id)
        emb: nextcord.Embed = nextcord.Embed(
            title=str(user),
            type="rich"
        )
        if banner := user.banner:
            emb.set_image(url=banner.url)
            await ctx.reply(
                embed=emb,
                allowed_mentions=nopings
            )
        else:
            await ctx.reply(
                content="No banner found",
                allowed_mentions=nopings
            )

    @commands.command(name="battery")
    async def battery(self, ctx):
        """
        Displays the status of the battery of the bot's host system
        """
        if not TERMUX:
            await ctx.reply(
                "This bot instance is not running under Termux",
                allowed_mentions=nopings
            )
            return

        async with ctx.channel.typing():
            out = subprocess.check_output(
                args="termux-battery-status",
                shell=True
            )
        data: dict = json.loads(out.decode("utf-8"))
        perc: int = data["percentage"]

        emoji: str = ""
        match(data["status"]):
            case "CHARGING":
                emoji = "⚡"
            case "FULL":
                emoji = "🔌"
            case "DISCHARGING":
                emoji = "🪫" if perc < 30 else "🔋"

        emb: nextcord.Embed = nextcord.Embed(
            type="rich",
            colour=0xFF0000 if perc < 30 else 0x0000FF,
            title="Battery percentage:",
            description=f"{emoji} Battery is at {perc}%"
        )

        await ctx.reply(
            embed=emb,
            allowed_mentions=nopings
        )

    @commands.command(name="banlist")
    @commands.has_permissions(manage_messages=True)
    async def banlist(self, ctx: commands.Context):
        """
        DMs the summoning user a text file with the current server's ban list
        """
        if not ctx.guild:
            raise Exception("Invalid Guild")

        bans = [entry async for entry in ctx.guild.bans(limit=2000)]
        bantxt = "\n".join(
            ["{} (ID:{})".format(str(x.user), x.user.id) for x in bans]
        )
        try:
            await ctx.author.send(
                file=nextcord.File(
                    io.BytesIO(bantxt.encode("utf-8")),
                    filename="bans.txt"
                )
            )
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply(
                content="An error has occurred, perhaps I'm blocked or you have DMs disabled for this server",
                allowed_mentions=nopings
            )

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *args: str):
        """
        Correct usage: ,eval <commands>
        Evaluates commands the inputted commands in a shell
        """
        async with ctx.channel.typing():
            out = subprocess.check_output(
                " ".join(args),
                shell=True
            )
        if len(out) < 1900:
            output = out.decode('utf-8').rstrip()
            answer = f"```{output}```" if output else "✅"

            await ctx.reply(
                content=answer,
                allowed_mentions=nopings
            )

        else:
            await ctx.reply(
                file=nextcord.File(
                    io.BytesIO(out),
                    filename="response.txt"
                )
            )

    @commands.command(name="escape")
    @commands.has_permissions(manage_messages=True)
    async def escape(self, ctx: commands.Context):
        """
        Correct usage <reply>,escape
        DMs a unicode escaped version of the replied message 
        and deletes the mention message afterwards.
        """
        if ctx.message.reference:
            id = ctx.message.reference.message_id
            if id is None:
                raise Exception("Invalid channel")

            message: nextcord.Message = await ctx.message.channel.fetch_message(id)

            await ctx.author.send(
                file=nextcord.File(
                    io.BytesIO(message.content.encode("unicode_escape")),
                    filename=f"unicode-escape-{ctx.message.id}.txt"
                )
            )
            await ctx.message.delete()
        else:
            await ctx.author.send("No reply found")
            await ctx.message.delete()

    @commands.command(name="pcbval_status")
    async def pcbval_status(self, ctx: commands.Context):
        """
        Returns the current uptime of the polcompballvalues backend server.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pcbval.theghostofinky.repl.co/uptime/") as resp:
                data = await resp.json()

        tstamp = datetime.datetime.fromisoformat(data["start_time"])
        raw_uptime = data["elapsed_time"]
        f_uptime = f"Backend online for: {raw_uptime['days']}d, "\
            f"{raw_uptime['hours']}h, {raw_uptime['minutes']}m, {raw_uptime['seconds']}s"

        emb = nextcord.Embed(
            title="Polcompballvalues backend uptime:",
            type="rich",
            description=f_uptime,
            color=0x99df96,
            timestamp=tstamp
        )
        await ctx.reply(
            embed=emb,
            allowed_mentions=nopings
        )


def setup(bot):
    bot.add_cog(utilities(bot))
