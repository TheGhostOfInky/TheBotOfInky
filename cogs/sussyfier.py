import os, discord, requests
from discord.ext import commands
import numpy as np
from PIL import Image
from random import randrange
output_width = 21  
twerk_frame_count = 6 
twerk_frames = []
twerk_frames_data = [] 
for i in range(6):
    img = Image.open(f"twerk_imgs/{i}.png").convert("RGBA")
    twerk_frames.append(img)
    twerk_frames_data.append(np.array(img))
twerk_width, twerk_height = twerk_frames[0].size

class sussyfier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="sussify")
    async def sussify(self, ctx, member: discord.Member=None):
        await sussy(ctx,member,False)

    @sussify.error
    async def sussify_error(error,ctx,message):
        await ctx.send(message)

    @commands.command(name="sussify_nn")
    async def sussify_nn(self, ctx, member: discord.Member=None):
        await sussy(ctx,member,True)

    @sussify_nn.error
    async def sussify_nn_error(error,ctx,message):
        await ctx.send(message)

async def sussy(ctx, member,nn):
    if member != None:
        await sus(ctx,member.avatar_url,"webp",nn)
    else:    
        async for message in ctx.channel.history(limit=100):
            if message.attachments:
                for attachment in message.attachments:
                    form = check_image(attachment.url)
                    if form:
                        await sus(ctx,attachment.url,form,nn)
                        return
            if message.embeds:
                for embed in message.embeds:
                    if embed.image.url:
                        form = check_image(embed.image.url)
                        if form:
                            await sus(ctx,embed.image.url,form,nn)
                            return
                    elif embed.url:
                        form = check_image(embed.url)
                        if form:
                            await sus(ctx,embed.url,form,nn)
                            return
        await ctx.send("No valid image found in the last 100 messages of the channel.")

def check_image(url):
    if ".png" in url:
        return "png"
    elif ".jpg" in url or ".jpeg" in url: 
        return "jpg"
    elif ".gif" in url:
        if "sussified.gif" in url:
            return False
        else:
            return "gif"
    elif ".webp" in url:
        return "webp"
    else:
        return False

async def sus(ctx,url,format,nearest_neighbour):
    seed = randrange(100000)
    message = await ctx.send(f"Found .{format}")    
    image = requests.get(url)
    file = open(f"temp/{seed}_input.{format}", "wb")
    file.write(image.content)
    file.close()
    input_image = Image.open(f"temp/{seed}_input.{format}").convert("RGB")
    await message.edit(content=f"Loaded .{format}")
    input_width, input_height = input_image.size
    output_height = int(output_width * (input_height / input_width) * (twerk_width / twerk_height))
    output_px = (int(output_width * twerk_width), int(output_height * twerk_height))
    if nearest_neighbour:
        input_image_scaled = input_image.resize((output_width, output_height), Image.NEAREST)
    else:
        input_image_scaled = input_image.resize((output_width, output_height))
    for frame_number in range(twerk_frame_count):
        await message.edit(content=f"Sussying frame # {frame_number}")
        background = Image.new(mode="RGBA", size=output_px)
        for y in range(output_height):
            for x in range(output_width):
                r, g, b = input_image_scaled.getpixel((x, y))
                sussified_frame_data = np.copy(twerk_frames_data[(x - y + frame_number) % len(twerk_frames)])
                red, green, blue, alpha = sussified_frame_data.T
                color_1 = (red == 214) & (green == 224) & (blue == 240)
                sussified_frame_data[..., :-1][color_1.T] = (r, g, b)  # thx stackoverflow
                color_2 = (red == 131) & (green == 148) & (blue == 191)
                sussified_frame_data[..., :-1][color_2.T] = (int(r*2/3), int(g*2/3), int(b*2/3))
                sussified_frame = Image.fromarray(sussified_frame_data)
                background.paste(sussified_frame, (x * twerk_width, y * twerk_height))
        background.save(f"temp/{seed}_sussified_{frame_number}.png")
    await message.edit(content="Converting sussy frames to sussy gif")
    os.system(f"ffmpeg -f image2 -i temp/{seed}_sussified_%d.png -filter_complex \"[0:v] scale=sws_dither=none:,split [a][b];[a] palettegen=max_colors=255:stats_mode=single [p];[b][p] paletteuse=dither=none\" -r 20 -y -hide_banner -loglevel error temp/{seed}_sussified.gif")
    with open(f"temp/{seed}_sussified.gif", 'rb') as f:
        amogus = discord.File(f)
        await message.delete()
        try:
            await ctx.send(file=amogus)
        except:
            await ctx.send("Failed to send gif.")
    for frame_number in range(twerk_frame_count):
        os.remove(f"temp/{seed}_sussified_{frame_number}.png")
    os.remove(f"temp/{seed}_sussified.gif")
    os.remove(f"temp/{seed}_input.{format}")

def setup(bot):
    bot.add_cog(sussyfier(bot))