import nextcord, sys
from nextcord.ext import commands
from base import nopings


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to discord')
        # sets status
        await self.bot.change_presence(
            activity=nextcord.Game(
                name=f"Running on Nextcord {nextcord.__version__} under Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        for attachment in message.attachments:
            if attachment.height == 1860 and attachment.width == 800:
                await message.reply(
                    content="Remember to submit your polcompballvalues scores using the "
                    '"Submit Your Scores" option at the bottom of the results '
                    "page if you want to be added to the user gallery.",
                    allowed_mentions=nopings
                )


def setup(bot):
    bot.add_cog(events(bot))
