import discord, json
from discord.ext import commands
with open("config/shield.json") as par_json:
    active_shields = json.load(par_json)

class shield(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if len(before.roles) < len(after.roles):
            delta = list(set(after.roles)-set(before.roles))
            if await check_filter(after,delta[0]):
                await after.remove_roles(delta[0],reason="Shield engaged",atomic=True)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def shield(self,ctx, member: discord.Member=None,role: discord.Role=None):
        if member==None or role==None:
            await ctx.send("Incorrect member and/or role specified")
        else:
            await ctx.send(await add_filter(member,role))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unshield(self,ctx, member: discord.Member=None,role: discord.Role=None):
        if member==None or role==None:
            await ctx.send("Incorrect member and/or role specified")
        else:
            await ctx.send(await remove_filter(member,role))

async def check_filter(user,newRole):
    global active_shields
    for server in active_shields:
        if server["id"] == str(user.guild.id):
            for member in server["members"]:
                if member["id"] == str(user.id):
                    for role in member["roles"]:
                        if role["id"] == str(newRole.id):
                            return True

async def add_filter(user,newRole):
    global active_shields
    for server in active_shields:
        if server["id"] == str(user.guild.id):
            for member in server["members"]:
                if member["id"] == str(user.id):
                    for role in member["roles"]:
                        if role["id"] == str(newRole.id):
                            return "Role already in shield"
                    return (await add_role(user,newRole))
            return (await add_member(user,newRole))
    return (await add_server(user,newRole))


async def add_server(user,newRole):
    global active_shields
    active_shields.append({"id":str(user.guild.id),"members":[]})
    return (await add_member(user,newRole))

async def add_member(user,newRole):
    global active_shields
    for server in active_shields:
        if server["id"] == str(user.guild.id):
            server["members"].append({"id":str(user.id),"roles":[]})
            return (await add_role(user,newRole))

async def add_role(user,newRole):
    global active_shields
    for server in active_shields:
        if server["id"] == str(user.guild.id):
            for member in server["members"]:
                if member["id"] == str(user.id):
                    member["roles"].append({"id":str(newRole.id)})
                    await jdump()
                    return f"Added role {newRole.name} and user {user} to filter"

async def remove_filter(user,newRole):
    if await check_filter(user,newRole):
        global active_shields
        for server in active_shields:
            if server["id"] == str(user.guild.id):
                for member in server["members"]:
                    if member["id"] == str(user.id):
                        for role in member["roles"]:
                            if role["id"] == str(newRole.id):
                                member["roles"].remove(role)
                                await jdump()
                                return f"Removed role {newRole.name} from filter"
    else:
        return "Role not shielded"    

async def jdump():
    with open("config/shield.json", "w") as par_json:
        json.dump(active_shields, par_json, indent=2, sort_keys=True)

def setup(bot):
    bot.add_cog(shield(bot))