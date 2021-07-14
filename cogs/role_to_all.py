import discord
from discord.ext import commands, tasks


class roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('role commands are ready')

    @commands.command(brief = "Cog testcommand")
    async def testcog_role(self, ctx):
        await ctx.send("Cog is loaded")

    @commands.command(brief = "Listázza az összes role-t a szerveren")
    @commands.has_role("admin")
    async def listallrole(self, ctx):
        roles = await ctx.guild.fetch_roles()
        msg = ""
        for x in roles:
            msg += f"{x.name}\n"
        await ctx.send(f"```{msg}```")

    @commands.command(brief = "<parancs> <rolename>")
    @commands.has_role("admin")
    async def addroletoall(self, ctx, rolename:str):
        members = await ctx.guild.fetch_members().flatten()
        roles = await ctx.guild.fetch_roles()
        for x in roles:
            if x.name == rolename:
                addedrole = x

        for ember in members:
            await ember.add_roles(addedrole)

def setup(client):
    client.add_cog(roles(client))

