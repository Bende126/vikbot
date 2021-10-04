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

class roleosch(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('roleosch is ready')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles = await after.guild.fetch_roles()
        for x in roles:
            if str(x.id) =="882332491363524628":
                generic_ev = x
            elif str(x.id) =="882337994223280220":
                generic_ga = x
            elif str(x.id) =="882337925524750356":
                generic_ka = x
            elif str(x.id) == "796698649815285760":
                gm_role = x

        if generic_ev in before.roles and generic_ev not in after.roles:
            for x in after.roles:
                if "Évfolyam: " in x.name:
                    await after.remove_roles(x)

        if generic_ga in before.roles and generic_ga not in after.roles:
            for x in after.roles:
                if "Gárda: " in x.name:
                    await after.remove_roles(x)
        
        if generic_ka in before.roles and generic_ka not in after.roles:
            for x in after.roles:
                if "Szak: " in x.name:
                    await after.remove_roles(x)

        await asyncio.sleep(3)

        for x in after.roles:
            if "Évfolyam: " in x.name:
                await after.add_roles(generic_ev)
            elif "Szak: " in x.name:
                await after.add_roles(generic_ka)
            elif "Gárda: " in x.name:
                await after.add_roles(generic_ga)
            elif str(x.id) in gm_roles:
                await after.add_roles(gm_role)

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

