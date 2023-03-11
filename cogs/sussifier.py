import nextcord, aiohttp, re, math, ffmpeg, dotenv, os, asyncio
import numpy as np
from base import nopings
from typing import Optional
from nextcord.ext import commands
from itertools import product
from PIL import Image
from PIL.Image import Image as Img
from io import BytesIO

dotenv.load_dotenv()

FRAMES_LOCATION = os.getenv("FRAMES_LOCATION") or "twerk_imgs"

cached_frames = []
cached_size = (0, 0)


def sus_pixel(pixel: tuple[int, int, int, int], frame: np.ndarray) -> Img:
    def adj(val):
        return math.floor(val * 2 / 3)

    r, g, b, a = pixel
    frame_data: np.ndarray = np.copy(frame)

    frame_data[
        np.all(frame_data == (214, 224, 240, 255), axis=-1)
    ] = (r, g, b, a)

    frame_data[
        np.all(frame_data == (131, 148, 191, 255), axis=-1)
    ] = (adj(r), adj(g), adj(b), a)

    frame_data[
        np.all(frame_data == (0, 0, 0, 255), axis=-1)
    ] = (0, 0, 0, a)

    frame_data[
        np.all(frame_data == (148, 201, 219, 255), axis=-1)
    ] = (148, 201, 219, a)

    return Image.fromarray(frame_data, mode="RGBA")


def sussify_frame(
        image: Img,
        frame_number: int,
        dimmensions: tuple[int, int],
        base_size: tuple[int, int],
        frames: list[np.ndarray],
        alpha: bool = False) -> Img:

    res = (dimmensions[0] * base_size[0], dimmensions[1] * base_size[1])
    frame = Image.new(mode="RGBA", size=res, color=(
        0, 0, 0, 0 if alpha else 255))

    for x, y in product(range(dimmensions[0]), range(dimmensions[1])):
        index = (x - y + frame_number) % len(frames)

        pixel = image.getpixel((x, y))
        selected_frame = frames[index]

        processed_pixel = sus_pixel(pixel, selected_frame)

        frame.paste(processed_pixel,
                    (x * base_size[0], y * base_size[1]), processed_pixel)

    return frame


def initialize(path: str, count: int = 6) -> tuple[list[np.ndarray], tuple[int, int]]:
    data: list[np.ndarray] = []

    size: tuple[int, int] = (0, 0)

    for i in range(count):
        image = Image.open(f"{path}/{i}.png").convert("RGBA")
        if i == 0:
            size = image.size

        data.append(np.array(image))

    return (data, size)


async def process_image(
        img_bytes: BytesIO,
        frames: list[np.ndarray],
        size: tuple[int, int],
        width: int = 21,
        nn: bool = False,
        alpha: bool = False) -> list[Img]:

    image = Image.open(img_bytes).convert("RGBA")

    w, h = image.size

    out_h = math.floor(width * (h / w) * (size[0] / size[1]))

    out = (width, out_h)
    scaled = image.resize(out, Image.NEAREST if nn else None)

    return await asyncio.gather(*[
        asyncio.to_thread(
            sussify_frame,
            scaled, x, out,
            size, frames, alpha
        ) for x in range(6)
    ])


async def transform(image: BytesIO, nn: bool = False, alpha: bool = False) -> BytesIO:
    global cached_frames, cached_size

    if not cached_frames:
        cached_frames, cached_size = await asyncio.to_thread(
            initialize, FRAMES_LOCATION
        )

    processed_frames = await process_image(
        image, cached_frames, cached_size, nn=nn, alpha=alpha
    )

    w, h = processed_frames[0].size

    files = [x.tobytes() for x in processed_frames]

    buff = BytesIO(b"".join(files))

    split = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="bgr32",
            s=f"{w}x{h}",
            framerate=20
        )
        .split()
    )
    palette = split[0].filter(
        "palettegen",
        reserve_transparent=1,
        max_colors=254,
        stats_mode="single"
    )
    final = (
        ffmpeg.filter(
            [split[1], palette],
            "paletteuse",
            alpha_threshold=128,
            dither="none"
        )
        .output("pipe:", format="gif")
        .global_args("-hide_banner")
        .global_args("-loglevel", "error")
        .run_async(
            pipe_stdin=True,
            pipe_stdout=True,
            pipe_stderr=True,
            quiet=True
        )
    )

    out, err = await asyncio.to_thread(final.communicate, input=buff.getbuffer())

    if err:
        with open("./logs/ffmpeg.log", "a") as l:
            l.write(err.decode("utf-8"))

    return BytesIO(out)


async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        return await response.read()


def find_image_message(message: nextcord.Message) -> Optional[str]:
    for attachment in message.attachments:
        if attachment.height is not None:
            return attachment.url

    for embed in message.embeds:
        if embed.image.url is not None:
            return embed.image.url

        if embed.thumbnail.url is not None:
            return embed.thumbnail.url


async def find_image_reply(ctx: commands.Context) -> Optional[str]:
    if not ctx.message.reference:
        return None

    id = ctx.message.reference.message_id
    if not id:
        return None

    ref = await ctx.message.channel.fetch_message(id)

    return find_image_message(ref)


async def find_image_history(ctx: commands.Context) -> Optional[str]:
    done = re.compile(r".+/sussified.gif$", flags=re.IGNORECASE | re.MULTILINE)

    async for message in ctx.channel.history(limit=100):
        msg_link = find_image_message(message)

        if msg_link and not done.match(msg_link):
            return msg_link


class SussifierFlags(commands.FlagConverter, case_insensitive=True):
    user: Optional[nextcord.Member] = None
    nn: bool = False
    alpha: bool = False


class sussifier(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="sussify")
    async def sussify(self, ctx: commands.Context, *, flags: SussifierFlags):
        """
        Correct usage ,sussify <user:@user> <nn:bool> <alpha:bool>
        Sussifies last image sent to channel or user avatar;
        nn: true disables image filtering, alpha: true enables transparency
        """
        async with ctx.channel.typing():
            if flags.user:
                img = flags.user.display_avatar.url
            else:
                img = await find_image_reply(ctx) \
                    or find_image_message(ctx.message) \
                    or await find_image_history(ctx)

            if img is None:
                await ctx.reply(
                    "No image found",
                    allowed_mentions=nopings
                )
                return

            async with aiohttp.ClientSession() as session:
                img_data = await fetch(session, img)

            sus_img = await (await asyncio.to_thread(
                transform, BytesIO(img_data), nn=flags.nn, alpha=flags.alpha))

            file = nextcord.File(sus_img, filename="sussified.gif")

        await ctx.reply(
            file=file,
            allowed_mentions=nopings
        )


def setup(bot):
    bot.add_cog(sussifier(bot))
