import discord, sys, re, json
from unidecode import unidecode
from discord.ext import commands
slurs = r"nigger(|s)|niggr|\bni..er(\b|s\b)|nigress|\bnegro|shitskin|fag\b|\bfag|fags\b|fagg|(f|fa|ph|pha)ggot|trann|trany|tranie|troon|troome|kike|chink|gook|sodomite|‎|​"
with open("config/filter.json") as par_json:
    filters = json.load(par_json)
filtered = []
for server in filters:
    filtered.append(server["id"])

class filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        global filtered
        if message.author.bot:
            return
        if str(message.guild.id) in filtered:
            if re.search(slurs, message.content, re.IGNORECASE):
                words = message.content.split(" ")
                matches = []
                for word in words:
                    if re.search(slurs, word, re.IGNORECASE):
                        matches.append(word)
                await message.delete()
                await sendwarn(message.author, matches)
                print("method 1")
            else:
                sentence = unidecode(message.content)
                if re.search(slurs, sentence, re.IGNORECASE):
                    words = sentence.split(" ")
                    matches = []
                    for word in words:
                        if re.search(slurs, word, re.IGNORECASE):
                            matches.append(word)
                    await message.delete()
                    await sendwarn(message.author, matches)
                    print("method 2")
                else:
                    sentence = re.sub(r"[^a-zA-Z\d]", "" ,sentence,  re.MULTILINE)
                    if re.search(slurs,sentence, re.IGNORECASE):
                        await message.delete()
                        await sendwarn(message.author,[])
                        print("method 3")

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enablefilter(self,ctx):
        global filters
        for server in filters:
            if server["id"] == str(ctx.guild.id):
                await ctx.send("Filter already enabled")
                return
        filters.append({"id":str(ctx.guild.id)})
        await jdump()
        await ctx.send("Filter enabled")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disablefilter(self,ctx):
        global filters
        for server in filters:
            if server["id"] == str(ctx.guild.id):
                filters.remove(server)
                await jdump()
                await ctx.send("Filter disabled")
                return
        await ctx.send("Filter already disabled")

async def jdump():
    global filters
    global filtered
    with open("config/filter.json", "w") as par_json:
        json.dump(filters, par_json, indent=2, sort_keys=True)
    filtered = []
    for server in filters:
        filtered.append(server["id"])

async def sendwarn(user, matches):
    if len(matches) == 1:
        if len(matches[0]) > 1950:
            await user.send("Watch your language")
            return
        await user.send(f"Watch your language, the word `{matches[0]}` is not allowed.")
    elif len(matches) > 1:
        matchstring = ""
        i = 0
        for match in matches:
            i += 1
            if len(matchstring) + len(match) > 1950:
                await user.send("Watch your language")
                return
            if i == len(matches):
                matchstring += " and `" + match + "`"
            else:
                matchstring += " `" + match + "`,"
        await user.send(f"Watch your language, the words {matchstring} are not allowed.")
    else:
        await user.send("Watch your language")

def setup(bot):
    bot.add_cog(filter(bot))