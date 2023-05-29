import nextcord, sys
from nextcord.ext import commands
from base import nopings


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to discord")

        # sets status
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        await self.bot.change_presence(
            activity=nextcord.Game(
                name=f"Running on Nextcord {nextcord.__version__} under Python {py_ver}"
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        for attachment in message.attachments:
            url = attachment.url.endswith("PCBValues.png")
            if url and attachment.width == 800 and attachment.height == 1000:
                await message.reply(
                    content="Remember to submit your PCBValues scores using the "
                    '"Submit Your Scores" option at the bottom of the results '
                    "page if you want to be added to the User Gallery.",
                    allowed_mentions=nopings
                )


def setup(bot):
    bot.add_cog(events(bot))
