import discord
from discord import emoji
from discord.enums import ContentFilter
from discord.ext import commands
from discord_slash import client, cog_ext, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_button, create_select, create_select_option
from discord_slash.model import ButtonStyle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import pytz
import asyncio

from trello import label

buttons = [
            create_button(
                style=ButtonStyle.green,
                label="A Green Button"
            ),
          ]

gm_roles = [
    "740528491367497781", #1. mc
    "796695732740554764", #2. csgo
    "796695564024283156", #3. lol
    "796696220286058516", #4. r6
    "796696319640993812", #5. amogus
    "894182437897244683", #6. rocket league
    "894183010759507978", #7. overwatch
    "894181680875712572" #8. apex
    ]

choice_ev = create_select(
    options=[
        create_select_option(label="Évfolyam: 2021", value="881250917113020488", emoji="🥼"),
        create_select_option(label="Évfolyam: 2020", value="881250853950996531", emoji="🧪"),
        create_select_option(label="Évfolyam: 2019", value="881250749521223680", emoji="🧫"),
        create_select_option(label="Évfolyam: 2018", value="882334562095607868", emoji="🦠"),
    ],
    custom_id="ev_select",
    placeholder="Évfolyamválasztó", 
    min_values=1, 
    max_values=1
)

choice_ga = create_select(
    options=[
        create_select_option(label="Gárda: Fekete", value="744645865825632296", emoji="🖤"),
        create_select_option(label="Gárda: Fehér", value="744644982396289219", emoji="🤍"),
        create_select_option(label="Gárda: Kék", value="744644137499885629", emoji="💙"),
        create_select_option(label="Gárda: Piros", value="744645871861366814", emoji="❤️"),
        create_select_option(label="Gárda: Sárga", value="744644695216619571", emoji="💛"),
    ],
    custom_id="garda_select",
    placeholder="Gárdaválasztó",  
    min_values=1,  
    max_values=1
)

choice_ka = create_select(
    options=[
        create_select_option(label="Szak: Mérnökinfó", value="739565921047150784", emoji="📱"),
        create_select_option(label="Szak: Villamosmérnök", value="739566045743939765", emoji="🚊"),
        create_select_option(label="Szak: Üzemmérnök", value="739566632803893329", emoji="🕹"),
    ],
    custom_id="szak_select",
    placeholder="Szakválasztó", 
    min_values=1, 
    max_values=1
)

choice_gm = create_select(
    options=[
        create_select_option(label="Minecraft Doomer", value="740528491367497781", emoji="💎"),
        create_select_option(label="CS:GO chad", value="796695732740554764", emoji="🔫"),
        create_select_option(label="League of Legends salt miner", value="796695564024283156", emoji="🦄"),
        create_select_option(label="Actual R6:Siege player", value="796696220286058516", emoji="🔫"),
        create_select_option(label="Valaki Among Us?", value="796696319640993812", emoji="🍖"),
        create_select_option(label="Rocket League sportsman", value="894182437897244683", emoji="🏎️🔥"),
        create_select_option(label="Overwatch abuser", value="894183010759507978", emoji="👼"),
        create_select_option(label="Apex enjoyer", value="894181680875712572", emoji="🔫"),
    ],
    custom_id="gm_select",
    placeholder="Géming roles",
    min_values=1,
    max_values=8
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
        await ctx.defer(hidden=True)
        roles = ctx.author.guild.roles
        member_roles = ctx.author.roles

        """if "Évfolyam: " in ctx.values[0]:
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

        await ctx.send(f"Ezt választottad: {ctx.values[0]}", hidden=True)"""



        selected_roles = discord.Embed(title = "Választott role(ok)",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow())

        for role in roles:
            if str(role.id) in ctx.values():
                await ctx.author.add_roles(role)      
                selected_roles.add_field(name=f"**{role.name}**", value=f"{role.mention}")

        if ctx.custom_id == "gm_select":
            for m_role in member_roles:
                if str(m_role.id) in gm_roles and str(m_role.id) not in ctx.values():
                    await ctx.author.remove_roles(m_role)

        await ctx.send(embed=selected_roles, hidden=True)

        thisjob = self.scheduler.add_job(self.cooldowntimer, run_date=(datetime.now())+timedelta(seconds=5), id=f"{ctx.author.name}", args=[ctx.author.name])
        print(str((datetime.now())+timedelta(seconds=5)))
        self.joblist.append(thisjob)
    
    """@commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles = await after.guild.fetch_roles()
        for x in roles:
            if str(x.name) =="Generic évfolyam":
                givenrole = x

        for x in after.roles:
            if "Évfolyam: " in x.name:
                await after.add_roles(givenrole)
                return"""

    @commands.command(hidden = True)
    async def ev_row(self, ctx):
        await ctx.send(content="Az év amikor felvettek ide", components=[create_actionrow(choice_ev)])

    @commands.command(hidden = True)
    async def ga_row(self, ctx):
        await ctx.send(content="A szín aminek tagja vagy", components=[create_actionrow(choice_ga)])

    @commands.command(hidden = True)
    async def ka_row(self, ctx):
        await ctx.send(content="Ebben a képzésben veszel részt", components=[create_actionrow(choice_ka)])

    @commands.command(hidden = True)
    async def gm_row(self, ctx):
        await ctx.send(content="Ilyen játékokkal játszol", components=[create_actionrow(choice_gm)])
    
    """@commands.command(hidden = True)
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

        await ctx.send("Done!")"""

def setup(client):
    client.add_cog(slash_command_support(client))
