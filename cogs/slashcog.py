import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option

choice_ev = create_select(
    options=[
        create_select_option("Évfolyam: 2021", value="Évfolyam: 2021", emoji="🥼"),
        create_select_option("Évfolyam: 2020", value="Évfolyam: 2020", emoji="🧪"),
        create_select_option("Évfolyam: 2019", value="Évfolyam: 2019", emoji="🧫"),
    ],
    placeholder="Évfolyamválasztó", 
    min_values=1, 
    max_values=1, 
)

choice_ga = create_select(
    options=[
        create_select_option("Gárda: Fekete", value="Gárda: Buckalakó", emoji="⚫️"),
        create_select_option("Gárda: Fehér", value="Gárda: Zacskós túró", emoji="⚪️"),
        create_select_option("Gárda: Kék", value="Gárda: Vikék", emoji="🔵"),
        create_select_option("Gárda: Piros", value="Gárda: Tűzvarázsló", emoji="🔴"),
        create_select_option("Gárda: Sárga", value="Gárda: #FF0", emoji="🟡"),
    ],
    placeholder="Gárdaválasztó",  
    min_values=1,  
    max_values=1,  
)

choice_ka = create_select(
    options=[
        create_select_option("Szak: Mérnökinfó", value="Szak: Mérnökinfó", emoji="📱"),
        create_select_option("Szak: Villamosmérnök", value="Szak: Villamosmérnök", emoji="🚊"),
        create_select_option("Szak: Üzemmérnök", value="Szak: Üzemmérnök", emoji="🕹"),
    ],
    placeholder="Szakválasztó", 
    min_values=1, 
    max_values=1, 
)

class slash_command_support(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('slashcog is ready')

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        roles = await ctx.guild.fetch_roles()

        if "Évfolyam: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Évfolyam: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        if "Gárda: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Gárda: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        if "Szak: " in ctx.values[0]:
            for x in ctx.author.roles:
                if "Szak: " in str(x.name):
                    await ctx.author.remove_roles(x)
            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)

        await ctx.send(f"Ezt választottad: {ctx.values[0]}", hidden=True)


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
    
    @commands.command(hidden = True)
    async def ev_row(self, ctx):
        await ctx.send(content="", components=[create_actionrow(choice_ev)])

    @commands.command(hidden = True)
    async def ga_row(self, ctx):
        await ctx.send(content="", components=[create_actionrow(choice_ga)])

    @commands.command(hidden = True)
    async def ka_row(self, ctx):
        await ctx.send(content="", components=[create_actionrow(choice_ka)])

def setup(client):
    client.add_cog(slash_command_support(client))
