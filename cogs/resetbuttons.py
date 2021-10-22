import discord
from discord.enums import ContentFilter
from discord.ext import commands
from discord_slash import client, cog_ext, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_button, create_select, create_select_option
from discord_slash.model import ButtonStyle

resetgombok = [
        create_button(
            style=ButtonStyle.red,
            label="Évfolyam reset",
            custom_id="882332491363524628"
        ),
        create_button(
            style=ButtonStyle.gray,
            label=" ",
            disabled=True
        ),
        create_button(
            style=ButtonStyle.red,
            label="Szak reset",
            custom_id="882337925524750356"
        ),
        create_button(
            style=ButtonStyle.gray,
            label=" ",
            disabled=True
        ),
        create_button(
            style=ButtonStyle.red,
            label="Gárda reset",
            custom_id="882337994223280220"
        )
]

class resetbuttons(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('resetbuttons is ready')

    @commands.command()
    async def testcog_resetbuttons(self, ctx):
        await ctx.send("Cog is ready")
    
    @commands.command(hidden=True)
    async def buttons(self, ctx):
        await ctx.send(content= "Visszaállítás, azaz reset gombok: ", components=[create_actionrow(*resetgombok)])

    @commands.Cog.listener()
    async def on_component(self,ctx: ComponentContext):
        if ctx.component_type == 3:
            return

        roles = ctx.author.guild.roles

        for x in roles:
            if int(ctx.custom_id) == x.id:
                await ctx.author.remove_roles(x)
                
        await ctx.send(content="Resetted role", hidden=True)

def setup(client):
    client.add_cog(resetbuttons(client))
