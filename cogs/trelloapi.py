import discord
from discord import embeds
from discord.embeds import EmbedProxy
from discord.ext import commands, tasks
from discord_slash import client, cog_ext, SlashContext
from datetime import datetime
import requests
from trello import TrelloClient
from trello.customfield import CustomFieldText

tclient = TrelloClient(
    api_key='',
    #api_secret='',
    token=''
)

pages_json = {}

list_options = [
    {
        "name":"listname",
        "description":"A lista neve",
        "required": True,
        "type":3
    },
    {
            "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    }

]

lists_options = [
    {
        "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    }

]

class trelloapi(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('trelloapi is ready')

    async def slide_right(self, member):
        global pages_json

        csanel = self.client.get_channel(pages_json[str(member.id)]["channel"])
        msg = await csanel.fetch_message(pages_json[str(member.id)]["message"])

        pages_json[str(member.id)]["current"] +=1

        print((pages_json[str(member.id)]["current"]))
        current = pages_json[str(member.id)]["current"]
        tembed = pages_json[str(member.id)]["pages"][current]
        pages = pages_json[str(member.id)]["pages"]

        await msg.edit(embed=tembed)
        await msg.clear_reactions()

        if current != 0 and current != (len(pages)-1):
            await msg.add_reaction("◀️")
            await msg.add_reaction("🟥")
            await msg.add_reaction("▶️")
        elif current == 0:
            await msg.add_reaction("🟥")
            await msg.add_reaction("▶️")
        elif current == (len(pages)-1):
            await msg.add_reaction("◀️")
            await msg.add_reaction("🟥")

        print("slided right")

    async def slide_left(self, member):
        global pages_json

        csanel = self.client.get_channel(pages_json[str(member.id)]["channel"])
        msg = await csanel.fetch_message(pages_json[str(member.id)]["message"])

        pages_json[str(member.id)]["current"] -=1

        print((pages_json[str(member.id)]["current"]))
        current = pages_json[str(member.id)]["current"]
        tembed = pages_json[str(member.id)]["pages"][current]
        pages = pages_json[str(member.id)]["pages"]

        await msg.edit(embed=tembed)
        await msg.clear_reactions()
        
        if current != 0 and current != (len(pages)-1):
            await msg.add_reaction("◀️")
            await msg.add_reaction("🟥")
            await msg.add_reaction("▶️")
        elif current == 0:
            await msg.add_reaction("🟥")
            await msg.add_reaction("▶️")
        elif current == (len(pages)-1):
            await msg.add_reaction("◀️")
            await msg.add_reaction("🟥")
        print("slided left")

    async def stop(self, member):
        csanel = self.client.get_channel(pages_json[str(member.id)]["channel"])
        msg = await csanel.fetch_message(pages_json[str(member.id)]["message"])
        await msg.delete(delay=None)
        print("stop")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)
        print("asd")

        if str(member.id) not in list(pages_json.keys()):
            return

        if(member == self.client.user or member.bot == True):
            return

        if payload.emoji.name == "◀️":
            await self.slide_left(member)
        elif payload.emoji.name =="🟥":
            await self.stop(member)
        elif payload.emoji.name =="▶️":
            await self.slide_right(member)

    @cog_ext.cog_slash(name="mytrello", description = "Listázza az általad csinált trello boardokat", guild_ids=[308599429122883586], options=None)
    async def mypolls_slash(self, ctx: SlashContext):
        all_boards = tclient.list_boards()
        for count, x in enumerate(all_boards):
            tboard = discord.Embed(
            title = f"Általad használt boardok",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow(),
            url = f"{x.url}")
            tboard.set_thumbnail(url= "https://mpng.subpng.com/20181107/vlx/kisspng-trello-app-store-macos-application-software-ios-5be2bc682da203.7081649815415860241869.jpg")
            tboard.add_field(name="Boardinfo", value=f"Name: {x.name}\nLeírás: {x.description}\nSorszám: {count+1}/{len(all_boards)}", inline=True)
            await ctx.send(embed=tboard, hidden = True)

    @cog_ext.cog_slash(name="createlist", description="Csinál egy listát egy adott boardon", options=list_options)
    async def createlist_slash(self, ctx: SlashContext, boardid =0, listname = ""):
        all_boards = tclient.list_boards()
        created_list = all_boards[boardid].add_list(name=listname)
        await ctx.send(content=f"Created list: {created_list}")

    @cog_ext.cog_slash(name="lists", description="Kiírja a listákat egy adott boardon", options=lists_options)
    async def lists_slash(self, ctx: SlashContext, boardid):
        global pages_json
        temp_pages = []
        temp_dict = {}

        all_boards = tclient.list_boards()
        """for x in all_boards:
            for y in x.all_lists():
                y.close()
                print(y.name)"""
        for lists in all_boards[boardid].all_lists():
            tlist = discord.Embed(
            title = f"List: {lists.name}",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow())

            for cards in lists.list_cards():
                tlist.add_field(name=cards.name, value=f"Név: {cards.name}\nLeírás: {cards.desc}\nLabel: {cards._labels}\nComments:{cards._comments}\nMembers:{cards.member_id}", inline=False)
            temp_pages.append(tlist)

        sentmsg = await ctx.send(embed=temp_pages[0])
        #await sentmsg.add_reaction("◀️")
        await sentmsg.add_reaction("🟥")
        await sentmsg.add_reaction("▶️")

        temp_dict["message"] = sentmsg.id
        temp_dict["pages"] = temp_pages
        temp_dict["current"] = 0
        temp_dict["channel"] = ctx.channel.id
        pages_json[str(ctx.author.id)] = temp_dict

    @commands.command()
    async def testcog_trelloapi(self, ctx):
        await ctx.send("Cog is ready")   

def setup(client):
    client.add_cog(trelloapi(client))

