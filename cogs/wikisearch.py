import nextcord, urllib.parse, aiohttp
from nextcord.ext import commands
from base import nopings
from typing import Union


class wikisearch(commands.Cog):
    """
    Returns search results from serveral wikis
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="pcbw", aliases=["pcb"])
    async def pcbw(self, ctx: commands.Context, *args) -> None:
        """
        Correct usage: ,pcbw/,pcb <search terms>
        Searches for matching pages in the Polcompball wiki
        """
        name: str = " ".join(args)
        await get_page(
            ctx=ctx,
            url="https://polcompball.miraheze.org",
            name=name
        )

    @commands.command(name="pcba")
    async def pcba(self, ctx: commands.Context, *args) -> None:
        """
        Correct usage: ,pcba <search terms>
        Searches for matching pages in the Polcompball Anarchy wiki
        """
        name: str = " ".join(args)
        await get_page(
            ctx=ctx,
            url="https://polcompballanarchy.miraheze.org",
            name=name
        )

    @commands.command(name="pcbm")
    async def pcbm(self, ctx: commands.Context, *args) -> None:
        """
        Correct usage: ,pcbm <search terms>
        Searches for matching pages in the Polcompball Minarchy wiki
        """
        name: str = " ".join(args)
        await get_page(
            ctx=ctx,
            url="https://polcompballminarchy.miraheze.org",
            name=name
        )

    @commands.command(name="wp", aliases=["wiki", "wikipedia"])
    async def wp(self, ctx: commands.Context, *args) -> None:
        """
        Correct usage: ,wp/,wiki/,wikipedia <search terms>
        Searches for matching pages in English Wikipedia
        """
        name: str = " ".join(args)
        await get_page(
            ctx=ctx,
            url="https://en.wikipedia.org",
            name=name
        )

    @commands.command(name="wt", aliases=["wiktionary"])
    async def wt(self, ctx: commands.Context, *args) -> None:
        """
        Correct usage: ,wt/,wiktionary <search terms>
        Searches for matching pages in English Wiktionary
        """
        name: str = " ".join(args)
        await get_page(
            ctx=ctx,
            url="https://en.wiktionary.org",
            name=name
        )


def stitch_url(url: str, page: str) -> str:
    return url + "/wiki/" + urllib.parse.quote(page.replace(" ", "_"))


async def get_data(url: str, params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            return await response.json()


async def get_wiki_page(url: str, name: str) -> Union[str, None]:
    pars: dict = {
        "action": "parse",
        "format": "json",
        "prop": "text",
        "utf8": "",
        "prop": "text=false",
        "page": name
    }
    apiurl: str = url + "/w/api.php"

    data: dict = await get_data(url=apiurl, params=pars)

    if "parse" in data:
        return data["parse"]["title"]
    else:
        return None


async def search_page(url: str, name: str) -> Union[nextcord.Embed, str, None]:
    pars: dict = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": "",
        "srprop": "snippet=false",
        "srsearch": name
    }
    apiurl: str = url + "/w/api.php"

    data: dict = await get_data(url=apiurl, params=pars)

    if data["query"]["search"]:
        embed: nextcord.Embed = nextcord.Embed(
            title="No page with this exact match was found, the following pages were found with related names:",
            colour=0x0000FF
        )

        for index, page in enumerate(data["query"]["search"]):
            if page["title"].lower() == name.lower():
                return (page["title"])

            embed.add_field(
                value=f"[{page['title']}]({stitch_url(url,page['title'])})",
                name="Match " + str(index + 1)
            )
        return embed
    else:
        return None


async def get_page(ctx: commands.Context, url: str, name: str):
    async with ctx.channel.typing():
        if page := await get_wiki_page(url=url, name=name):
            await ctx.reply(
                content=stitch_url(url, page),
                allowed_mentions=nopings
            )
        elif rep := await search_page(url=url, name=name):
            if isinstance(rep, str):
                await ctx.reply(
                    content=stitch_url(url, rep),
                    allowed_mentions=nopings
                )
            else:
                await ctx.reply(
                    embed=rep,
                    allowed_mentions=nopings
                )
        else:
            await ctx.reply(
                content="No matching pages were found",
                allowed_mentions=nopings
            )
        return


def setup(bot):
    bot.add_cog(wikisearch(bot))
