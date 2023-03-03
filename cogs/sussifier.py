import nextcord, aiohttp, re, math, ffmpeg, dotenv, os
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


def sus_pixel(pixel: tuple[int, int, int], frame: np.ndarray) -> Img:
    def adj(val):
        return math.floor(val * 2 / 3)

    r, g, b = pixel
    frame_data = np.copy(frame)
    red, green, blue, *_ = frame_data.T

    color_1 = (red == 214) & (green == 224) & (blue == 240)
    frame_data[..., :-1][color_1.T] = (r, g, b)

    color_2 = (red == 131) & (green == 148) & (blue == 191)
    frame_data[..., :-1][color_2.T] = (adj(r), adj(g), adj(b))

    return Image.fromarray(frame_data)


def sussify_frame(
        image: Img,
        frame_number: int,
        dimmensions: tuple[int, int],
        base_size: tuple[int, int],
        frames: list[np.ndarray]) -> Img:

    res = (dimmensions[0] * base_size[0], dimmensions[1] * base_size[1])
    frame = Image.new(mode="RGBA", size=res)

    for x, y in product(range(dimmensions[0]), range(dimmensions[1])):
        index = (x - y + frame_number) % len(frames)

        pixel = image.getpixel((x, y))
        selected_frame = frames[index]

        processed_pixel = sus_pixel(pixel, selected_frame)

        frame.paste(processed_pixel, (x * base_size[0], y * base_size[1]))

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


def process_image(
        img_bytes: BytesIO,
        frames: list[np.ndarray],
        size: tuple[int, int],
        width: int = 21,
        nn: bool = False) -> list[Img]:

    image = Image.open(img_bytes).convert("RGB")

    w, h = image.size

    out_h = math.floor(width * (h / w) * (size[0] / size[1]))

    out = (width, out_h)
    scaled = image.resize(out, Image.NEAREST if nn else None)

    return [
        sussify_frame(scaled, x, out, size, frames) for x in range(6)
    ]


def transform(image: BytesIO, nn: bool = False) -> BytesIO:
    global cached_frames, cached_size

    if not cached_frames:
        cached_frames, cached_size = initialize(FRAMES_LOCATION)

    processed_frames = process_image(
        image, cached_frames, cached_size, nn=nn
    )

    w, h = processed_frames[0].size

    files = [x.tobytes() for x in processed_frames]

    buff = BytesIO(b"".join(files))

    streams = (
        ffmpeg.input(
            "pipe:",
            format="rawvideo",
            pix_fmt="bgr32",
            s=f"{w}x{h}",
            framerate=20
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

    out, err = streams.communicate(input=buff.getbuffer())

    if err:
        with open("./logs/ffmpeg.log", "a") as l:
            l.write(err.decode("utf-8"))

    return BytesIO(out)


async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        return await response.read()


async def find_image(ctx: commands.Context) -> Optional[str]:
    done = re.compile(r".+/sussified.gif$", flags=re.IGNORECASE | re.MULTILINE)
    pattern = re.compile(r".+\.(png|gif|jpg|jpeg|webp|tiff)$",
                         flags=re.IGNORECASE | re.MULTILINE)
    async for messasge in ctx.channel.history(limit=100):
        if not messasge.attachments:
            continue
        for attachment in messasge.attachments:
            if done.match(attachment.url):
                continue
            if pattern.match(attachment.url):
                return attachment.url


async def find_image_current(ctx: commands.Context) -> Optional[str]:
    pattern = re.compile(r".+\.(png|gif|jpg|jpeg|webp|tiff)$",
                         flags=re.IGNORECASE | re.MULTILINE)
    if not ctx.message.attachments:
        return
    for attachment in ctx.message.attachments:
        if pattern.match(attachment.url):
            return attachment.url


class SussifierFlags(commands.FlagConverter):
    nn: bool = False
    user: Optional[nextcord.Member]


class sussifier(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="sussify")
    async def sussify(self, ctx: commands.Context, flags: SussifierFlags):
        """
        Correct usage ,sussify <nn:bool> <user:@user>
        Sussifies last image sent to channel or user avatar; nn:True disables image filtering
        """
        async with ctx.channel.typing():
            if flags.user:
                img = flags.user.display_avatar.url
            else:
                img = await find_image_current(ctx) \
                    or await find_image(ctx)

            if img is None:
                await ctx.reply(
                    "No image found",
                    allowed_mentions=nopings
                )
                return

            async with aiohttp.ClientSession() as session:
                img_data = await fetch(session, img)

            sus_img = transform(BytesIO(img_data), nn=flags.nn)

            file = nextcord.File(sus_img, filename="sussified.gif")

        await ctx.reply(
            file=file,
            allowed_mentions=nopings
        )


def setup(bot):
    bot.add_cog(sussifier(bot))
