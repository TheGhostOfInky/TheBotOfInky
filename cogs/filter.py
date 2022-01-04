import discord, sys, re, json
from unidecode import unidecode
from discord.ext import commands
with open("config/filter.json") as par_json:
    filters = json.load(par_json)
slurs = r"ni(.)\1{1,}er|niggr|\bni..er(\b|s\b)|fag\b|\bfag|(f|p)hag|\b(p|f)hg\b|(p|f)ahg|fags\b|fa(g)\1{1,}|(f|fa|fi|fh|ph|pha)(g)\1{1,}|thrann(y|ie)|tr(ha|ah)nn(y|ie)|trahnn(y|ie)|trann|trany|tranie|tr(o)\1{1,}(n|m)|k(i|1|l)ke|nigress|\bnegro|shitskin|chink|g(o)\1{1,}k|sodomite|‎|​|‏"
class filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    #Listens to slurs
    @commands.Cog.listener()
    async def on_message(self, message):
        thisMess = message
        if thisMess.channel.type != discord.ChannelType.text:
            return
        elif await ch_filter(thisMess):
            await scanmessage(thisMess)
    #Listens to slurs on edited messages 
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        thisMess = after
        if thisMess.channel.type != discord.ChannelType.text:
            return
        elif await ch_filter(thisMess):
            await scanmessage(thisMess)

    #servers

    @commands.command(name="enablefilter")
    @commands.has_permissions(administrator=True)
    async def enablefilter(self,ctx):
        gid = str(ctx.guild.id)
        if gid in filters["servers"]:
            if filters["servers"][gid]["filter"]:
                await ctx.send("Filter already enabled")
                return
        filters["servers"][gid]={'filter': True, 'whitelisted_channels': [], 'whitelisted_roles': [], 'whitelisted_users': []}
        await jdump()
        await ctx.send("Filter enabled")

    @commands.command(name="disablefilter")
    @commands.has_permissions(administrator=True)
    async def disablefilter(self,ctx):
        gid = str(ctx.guild.id)
        if gid in filters["servers"]:
            if filters["servers"][gid]["filter"]:
                filters["servers"][gid]["filter"] = False
                await jdump()
                await ctx.send("Filter disabled")
                return
            await ctx.send("Filter already disabled")
    
    #channels

    @commands.command(name="whitelist_channel")
    @commands.has_permissions(administrator=True)
    async def whitelist_channel(self,ctx,channel: discord.TextChannel=None):
        if channel == None:
            await ctx.send("No channel specified")
            return
        gid = str(ctx.guild.id)
        cid = str(channel.id)
        if gid in filters["servers"]:
            if cid in filters["servers"][gid]["whitelisted_channels"]:
                await ctx.send("Channel already whitelisted")
                return
            else:
                filters["servers"][gid]["whitelisted_channels"].append(cid)
        else:
            filters["servers"][gid]={'filter': False, 'whitelisted_channels': [cid], 'whitelisted_roles': [], 'whitelisted_users': []}
        await jdump()
        await ctx.send(f"Channel {str(channel)} whitelisted")

    @commands.command(name="dewhitelist_channel")
    @commands.has_permissions(administrator=True)
    async def dewhitelist_channel(self,ctx,channel: discord.TextChannel=None):
        if channel == None:
            await ctx.send("No channel specified")
            return
        gid = str(ctx.guild.id)
        cid = str(channel.id)
        if gid in filters["servers"]:
            if cid in filters["servers"][gid]["whitelisted_channels"]:
                filters["servers"][gid]["whitelisted_channels"].remove(cid)
                await jdump()
                await ctx.send(f"Channel {str(channel)} dewhitelisted")
                return
        await ctx.send("Channel not whitelisted")

    #roles

    @commands.command(name="whitelist_role")
    @commands.has_permissions(administrator=True)
    async def whitelist_role(self,ctx,role: discord.Role=None):
        if role == None:
            await ctx.send("No role specified")
            return
        gid = str(ctx.guild.id)
        rid = str(role.id)
        if gid in filters["servers"]:
            if rid in filters["servers"][gid]["whitelisted_roles"]:
                await ctx.send("Role already whitelisted")
                return
            else:
                filters["servers"][gid]["whitelisted_roles"].append(rid)
        else:
            filters["servers"][gid]={'filter': False, 'whitelisted_channels': [], 'whitelisted_roles': [rid], 'whitelisted_users': []}
        await jdump()
        await ctx.send(f"Role {str(role)} whitelisted")

    @commands.command(name="dewhitelist_role")
    @commands.has_permissions(administrator=True)
    async def dewhitelist_role(self,ctx,role: discord.Role=None):
        if role == None:
            await ctx.send("No channel specified")
            return
        gid = str(ctx.guild.id)
        rid = str(role.id)
        if gid in filters["servers"]:
            if rid in filters["servers"][gid]["whitelisted_roles"]:
                filters["servers"][gid]["whitelisted_roles"].remove(rid)
                await jdump()
                await ctx.send(f"Role {str(role)} dewhitelisted")
                return
        await ctx.send("Role not whitelisted")

    #users

    @commands.command(name="whitelist_user")
    @commands.has_permissions(administrator=True)
    async def whitelist_user(self,ctx,user: discord.Member=None):
        if user == None:
            await ctx.send("No user specified")
            return
        gid = str(ctx.guild.id)
        uid = str(user.id)
        if gid in filters["servers"]:
            if uid in filters["servers"][gid]["whitelisted_users"]:
                await ctx.send("User already whitelisted")
                return
            else:
                filters["servers"][gid]["whitelisted_users"].append(uid)
        else:
            filters["servers"][gid]={'filter': False, 'whitelisted_channels': [], 'whitelisted_roles': [], 'whitelisted_users': [uid]}
        await jdump()
        await ctx.send(f"User {str(user)} whitelisted")

    @commands.command(name="dewhitelist_user")
    @commands.has_permissions(administrator=True)
    async def dewhitelist_user(self,ctx,user: discord.Member=None):
        if user == None:
            await ctx.send("No user specified")
            return
        gid = str(ctx.guild.id)
        uid = str(user.id)
        if gid in filters["servers"]:
            if uid in filters["servers"][gid]["whitelisted_users"]:
                filters["servers"][gid]["whitelisted_users"].remove(uid)
                await jdump()
                await ctx.send(f"User {str(user)} dewhitelisted")
                return
        await ctx.send("User not whitelisted")
    
    #Error handling

    @enablefilter.error
    async def enablefilter_error(error,ctx,message):
        await ctx.send(message)
    @disablefilter.error
    async def disablefilter_error(error,ctx,message):
        await ctx.send(message)
    @whitelist_channel.error
    async def whitelist_channel_error(error,ctx,message):
        await ctx.send(message)
    @dewhitelist_channel.error
    async def dewhitelist_channel_error(error,ctx,message):
        await ctx.send(message)
    @whitelist_role.error
    async def whitelist_role_error(error,ctx,message):
        await ctx.send(message)
    @dewhitelist_role.error
    async def dewhitelist_role_error(error,ctx,message):
        await ctx.send(message)
    @whitelist_user.error
    async def whitelist_user_error(error,ctx,message):
        await ctx.send(message)
    @dewhitelist_user.error
    async def dewhitelist_user_error(error,ctx,message):
        await ctx.send(message)

#code outside of class

async def ch_filter(message):
    if str(message.guild.id) in filters["servers"]:
         if filters["servers"][str(message.guild.id)]["filter"]:
            if str(message.channel.id) not in filters["servers"][str(message.guild.id)]["whitelisted_channels"]:
                if message.author.discriminator == "0000":
                    return True
                elif str(message.author.id) not in filters["servers"][str(message.guild.id)]["whitelisted_users"]:
                    for role in message.author.roles:
                        if str(role.id) in filters["servers"][str(message.guild.id)]["whitelisted_roles"]:
                            return False
                    return True
    return False

async def scanmessage(thisMess):
    match = await findmatch(thisMess,thisMess.content,True)
    if not match:
        sentence = unidecode(thisMess.content)
        match = await findmatch(thisMess,sentence,True)
        if not match:
            sentence = re.sub(r"[^a-zA-Z\d]", "" ,sentence,  re.MULTILINE)
            match = await findmatch(thisMess,sentence,False)


async def findmatch(message,contents,listed):
    if re.search(slurs, contents, re.IGNORECASE):
        await message.delete()
        if listed:
            words = message.content.split(" ")
            matches = []
            for word in words:
                if re.search(slurs, word, re.IGNORECASE):
                    matches.append(word)
            await sendwarn(message.author, matches)
        else:
            await sendwarn(message.author, [])
        return True
    else:
        return False

async def sendwarn(user, matches):
    if user.bot:
        return
    warnStr = "Watch your language"
    if len(matches) == 1 and len(matches[0]) < 1950:
            warnStr = f"Watch your language, the word `{matches[0]}` is not allowed."
    elif len(matches) > 1:
        matchstring = ""
        i = 0
        for match in matches:
            i += 1
            if len(matchstring) + len(match) < 1950:
                if i == len(matches):
                    matchstring += " and `" + match + "`"
                else:
                    matchstring += " `" + match + "`,"
        if len(matchstring) > 0:
            warnStr = f"Watch your language, the words {matchstring} are not allowed."
    try:
        await user.send(warnStr)
    except:
        print(f"Error occurred when sending warn to {str(user)}")

async def jdump():
    with open("config/filter.json", "w") as par_json:
        json.dump(filters, par_json, indent=2, sort_keys=True)

def setup(bot):
    bot.add_cog(filter(bot))