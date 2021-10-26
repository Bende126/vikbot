import discord
from discord.ext import commands, tasks
import asyncio

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

ev_roles = [
    "882334562095607868", #2018
    "881250749521223680", #2019
    "881250853950996531", #2020
    "881250917113020488"  #2021
]

ka_roles=[
    "739566045743939765", #villany
    "739565921047150784", #mérnök
    "739566632803893329"  #üzem
]

ga_roles = [
    "744645871861366814", #piros 
    "744644137499885629", #kék
    "744645865825632296", #fekete
    "744644982396289219", #fehér
    "744644695216619571"  #sárga
]

class roleosch(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('roleosch is ready')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id != 737284142462402560:
            return

        bfroles = before.roles
        afroles = after.roles
        
        bfroles.sort()
        afroles.sort()

        if bfroles == afroles:
            return 
        #roles = await after.guild.fetch_roles()
        roles = before.guild.roles
        print(roles)
        generic_ev = generic_ga = generic_ka = gm_role = None
        addedroles = []
        removedroles = []
        #print(roles)
        for x in roles:
            if str(x.id) =="882332491363524628":
                generic_ev = x
            elif str(x.id) =="882337994223280220":
                generic_ga = x
            elif str(x.id) =="882337925524750356":
                generic_ka = x
            elif str(x.id) == "796698649815285760":
                gm_role = x

        if generic_ev==None or generic_ga==None or generic_ka==None or gm_role ==None:
            print("failed to load roles")
            return

        if generic_ev in before.roles and generic_ev not in after.roles:
            for x in after.roles:
                if str(x.id) in ev_roles:
                    removedroles.append(x)
                    #await asyncio.sleep(0.5)

        if generic_ga in before.roles and generic_ga not in after.roles:
            for x in after.roles:
                if str(x.id) in ga_roles:
                    removedroles.append(x)
                    #await asyncio.sleep(0.5)
        
        if generic_ka in before.roles and generic_ka not in after.roles:
            for x in after.roles:
                if str(x.id) in ka_roles:
                    removedroles.append(x)
                    #await asyncio.sleep(0.5)

        for x in after.roles:
            if str(x.id) in ev_roles:
                #await after.add_roles(generic_ev)
                addedroles.append(x)
                #await asyncio.sleep(0.5)
            elif str(x.id) in ka_roles:
                #await after.add_roles(generic_ka)
                #await asyncio.sleep(0.5)
                addedroles.append(x)
            elif str(x.id) in ga_roles:
                #await after.add_roles(generic_ga)
                #await asyncio.sleep(0.5)
                addedroles.append(x)
            elif str(x.id) in gm_roles:
                #await after.add_roles(gm_role)
                #await asyncio.sleep(0.5)
                addedroles.append(x)
        await after.remove_roles(*removedroles)
        print("added roles")
        await after.add_roles(*addedroles)
        print("removed roles")

    @commands.command()
    async def testcog_roleosch(self, ctx):
        await ctx.send("Cog is ready")

    @commands.command(hidden = True)
    async def check_roles(self, ctx):
        emberek = await ctx.guild.fetch_members().flatten()
        roles = await ctx.guild.fetch_roles()

        for x in roles:
            if str(x.name) =="Generic évfolyam":
                generic_ev = x
            elif str(x.name) =="Generic gárda":
                generic_ga = x
            elif str(x.name) =="Generic szak":
                generic_ka = x

        for ember in emberek:
            for y in ember.roles:
                if "Gárda: " in y.name:
                    await ember.add_roles(generic_ga)
                    await asyncio.sleep(0.1)

                elif "Szak: " in y.name:
                    await ember.add_roles(generic_ka)
                    await asyncio.sleep(0.1)
            
                elif "Évfolyam: " in y.name:
                    await ember.add_roles(generic_ev)
                    await asyncio.sleep(0.1)
                    
        await ctx.send("Done!")

def setup(client):
    client.add_cog(roleosch(client))

