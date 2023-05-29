import os, nextcord, dotenv, datetime, logging
from nextcord.ext import commands
from base import nopings

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")
PREFIX = os.getenv("DISCORD_PREFIX", "$")
intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
COGS = ["events", "utilities", "ban-purger",
        "wikisearch", "emojilister", "sussifier"]
for cog in COGS:
    bot.load_extension("cogs." + cog)


@bot.event
async def on_disconnect():
    time = datetime.datetime.now()
    logging.log(logging.INFO, f"Disconnected at {time}")


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    else:
        await ctx.reply(
            content=f"Command errored with the following error: \n```{error}```",
            allowed_mentions=nopings
        )


def main():
    logger = logging.getLogger('nextcord')
    logger.setLevel(logging.INFO)

    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    os.makedirs("./logs", exist_ok=True)

    handler = logging.FileHandler(
        filename=f"./logs/discord-{date}.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
