import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext

class slash_command_support(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('slashcog is ready')

    @commands.command()
    async def testcog_slashcommands(self, ctx):
        await ctx.send("Cog is ready")
    
    ping_options = [
        {
            "name":"joke",
            "description":"Joke része a dolognak",
            "required": False,
            "type":5
        }
    ]

    @cog_ext.cog_slash(name="ping", description = "Tells you the ping", guild_ids = [308599429122883586], options = ping_options)
    async def test(self, ctx: SlashContext, joke = True):
        #await ctx.defer()
        if(joke):
            await ctx.send(content = "Pong!", hidden= False)
        else:
            await ctx.send(content=f"A ping az {round(self.client.latency*1000)}ms", hidden= True)

def setup(client):
    client.add_cog(slash_command_support(client))
