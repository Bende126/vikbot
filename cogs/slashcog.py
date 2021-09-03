import discord
from discord.ext import commands
from discord_slash import client, cog_ext, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_button, create_select, create_select_option
from discord_slash.model import ButtonStyle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import asyncio

buttons = [
            create_button(
                style=ButtonStyle.green,
                label="A Green Button"
            ),
          ]

select = create_select(
    options=[# the options in your dropdown
        create_select_option("Évfolyam: 2021", value="Évfolyam: 2021", emoji="🥼"),
        create_select_option("Évfolyam: 2020", value="Évfolyam: 2020", emoji="🧪"),
        create_select_option("Évfolyam: 2019", value="Évfolyam: 2019", emoji="🧫"),
        create_select_option("Évfolyam: 2018", value="Évfolyam: 2018", emoji="🦠"),
    ],
    placeholder="Évfolyamválasztó",  # the placeholder text to show when no options have been chosen
    min_values=1,  # the minimum number of options a user must select
    max_values=1,  # the maximum number of options a user can select
)

class slash_command_support(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler()
        self.joblist=[]
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('slashcog is ready')
        self.scheduler.start()

    @commands.command()
    async def testcog_slashcommands(self, ctx):
        await ctx.send("Cog is ready")

    async def cooldowntimer(self, name):
        print("Job done")
        for x in self.joblist:
            if x.id == name:
                self.joblist.remove(x)

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

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        # ctx.selected_options is a list of all the values the user selected
        #await ctx.send(content=f"You selected {ctx.selected_options}")
        #await ctx.edit_origin(content="You pressed a button!")
        for x in self.joblist:
            if x.id == str(ctx.author.name):
                await ctx.send(f"Még várj ennyi időegységet(másodpercet) légyszi: {str((x.next_run_time)-pytz.utc.localize(datetime.now()))[14:-7]}", hidden=True)
            return

        roles = await ctx.guild.fetch_roles()

        if "Évfolyam: " in ctx.values[0]:

            for x in ctx.author.roles:
                if "Évfolyam: " in str(x.name):
                    print(x.name)
                    await ctx.author.remove_roles(x)

            for x in roles:
                if str(x.name) == ctx.values[0]:
                    await ctx.author.add_roles(x)
        await ctx.send(f"Ezt választottad: {ctx.values[0]}", hidden=True)
        
        thisjob = self.scheduler.add_job(self.cooldowntimer, run_date=(datetime.now())+timedelta(seconds=20), id=f"{ctx.author.name}", args=[ctx.author.name])
        print(str((datetime.now())+timedelta(seconds=20)))
        self.joblist.append(thisjob)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles = await after.guild.fetch_roles()
        for x in roles:
            if str(x.name) =="Generic évfolyam":
                givenrole = x

        for x in after.roles:
            if "Évfolyam: " in x.name:
                await after.add_roles(givenrole)
                return

    @commands.command(hidden = True)
    async def test_row(self, ctx):
        await ctx.send("Válassz évfolyamot!", components=[create_actionrow(select)])  # like action row with buttons but without * in front of the variable
    
    @commands.command(hidden = True)
    async def check_roles(self, ctx):
        emberek = await ctx.guild.fetch_members().flatten()
        roles = await ctx.guild.fetch_roles()
        for ember in emberek:
            for y in ember.roles:
                if "Gárda: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic gárda":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)

                if "Szak: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic szak":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)
            
                if "Évfolyam: " in y.name:
                    for z in roles:
                        if str(z.name) == "Generic évfolyam":
                            await ember.add_roles(z)
                            await asyncio.sleep(0.1)
        await ctx.send("Done!")

"""
    @cog_ext.cog_subcommand(base="prefix", name="add", description="todo")
    async def prefix_add(self, ctx: SlashContext):
        ctx.send(content="asdfghj", hidden=True)

    @cog_ext.cog_subcommand(base="prefix", name="remove", description="todo")
    async def prefix_remove(self, ctx: SlashContext):
        ctx.send(content="asdfghj", hidden=True)

    @cog_ext.cog_subcommand(base="prefix", name="list", description="todo")
    async def prefix_list(self, ctx: SlashContext):
        ctx.send(content="asdfghj", hidden=True)
    
    @cog_ext.cog_subcommand(base="cog", name="add", description="todo")
    async def cog_add(self, ctx: SlashContext):
        ctx.send(content="asdfghj", hidden=True)

    @cog_ext.cog_subcommand(base="cog", name="remove", description="todo")
    async def cog_remove(self, ctx: SlashContext):
        ctx.send(content="asdfghj", hidden=True)
    
    @cog_ext.cog_subcommand(base="cog", name="list", description="todo")
    async def cog_list(self, ctx: SlashContext):
        coglist = "vlami ide"
        ctx.send(content=coglist, hidden=True)
"""
def setup(client):
    client.add_cog(slash_command_support(client))
