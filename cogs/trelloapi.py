from re import T
import discord
from discord import embeds
from discord.embeds import EmbedProxy
from discord.ext import commands, tasks
from discord.ext.commands.errors import NoEntryPointError
from discord.team import Team
from discord_slash import client, cog_ext, SlashContext
from datetime import datetime
from trello import TrelloClient, board, card, member
from trello.customfield import CustomFieldText
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import pickle
import asyncio

password_provided = "asdw"  
password = password_provided.encode()  
salt = b'\x81t\xd4C+\x92\x82O\xd0\x18du\xb6}\xcd\x7f'

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
    },
    {
        "name":"position",
        "description":"A lista pozíciója a boardon",
        "required": False,
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

login_options = [
    {
        "name":"api_key",
        "description":"Trello api kulcsa a fiókodnak",
        "required": True,
        "type":3
    },
    {
        "name":"api_secret",
        "description":"Trello api secretje a fiókodnak",
        "required": True,
        "type":3
    },
    {
        "name": "token",
        "description":"Trello tokenje a fiókodnak",
        "required": True,
        "type":3
    }

]

comment_options= [
    {
        "name": "comment",
        "description":"Comment amit te szeretnél írni",
        "required": True,
        "type":3
    },
    {
        "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"listid",
        "description":"A list sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"cardid",
        "description":"A card sorszáma",
        "required": True,
        "type":4
    }
]

createcard_options = [
    {
        "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"listid",
        "description":"A list sorszáma",
        "required": True,
        "type":4
    },
        {
        "name":"name",
        "description":"A card neve",
        "required": True,
        "type":3
    },
        {
        "name":"description",
        "description":"A card leírása",
        "required": False,
        "type":3
    },
        {
        "name":"clonefrom",
        "description":"Ha cardot szeretnél klónozni",
        "required": False,
        "type":4
    },
        {
        "name":"position",
        "description":"Ha specifikus helyre szeretnéd rakni",
        "required": False,
        "type":4
    }
]

editlist_options=[
    {
        "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"listid",
        "description":"A list sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"name",
        "description":"A list új neve",
        "required": False,
        "type":3
    },
    {
        "name":"position",
        "description":"A lista pozíciója",
        "required": False,
        "type":4
    },
    {
        "name":"closed",
        "description":"Ha True, akkor archiválja a listet",
        "required": False,
        "type":5
    }

]

editcard_options = [
        {
        "name":"boardid",
        "description":"A board sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"listid",
        "description":"A list sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"cardid",
        "description":"A card sorszáma",
        "required": True,
        "type":4
    },
    {
        "name":"changelist",
        "description":"A list sorszáma, ahova áthelyezed",
        "required": False,
        "type":4
    },
    {
        "name":"changepos",
        "description":"A card sorszáma a listen belül",
        "required": False,
        "type":4
    },
    {
        "name":"delete",
        "description":"Ha True, akkor törölni fogja a cardot",
        "required": False,
        "type":5
    },
    {
        "name":"name",
        "description":"A card új neve",
        "required": False,
        "type":3
    }
]

def get_client(memberid):
    tempdict = load_token()
    for keys in tempdict:
        if keys == str(memberid):
            accesdict = tempdict[keys]
    tclient = TrelloClient(
    api_key=accesdict["api"],
    api_secret=accesdict["secret"],
    token=accesdict["token"]
    )

    print("got client")
    return tclient

def save_token(tempdict):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    loadedtoken = load_token()
    #saveddict = {**tempdict, **loadedtoken}
    saveddict = loadedtoken.copy()
    saveddict.update(tempdict)
    print(saveddict)

    toencrypt = json.dumps(saveddict).encode()
    encrypted = f.encrypt(toencrypt).decode()

    with open("trello/token.json", "w") as fp:
        json.dump(encrypted, fp)

    print("saved token")

def load_token():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    with open("trello/token.json", "r") as fp:
        loadeddict = json.loads(fp.read())

    todecrypt = json.dumps(loadeddict).encode()
    returndict = f.decrypt(todecrypt).decode()

    print(json.loads(returndict))
    #print(f"\n{key}\n")
    return json.loads(returndict)

def load_embed():
    with open("trello/embed.pickle","rb") as fp:
        tempdict = pickle.load(fp)
    return tempdict

def save_embed(tempdict):
    loadedpickle = load_embed()
    tosave = loadedpickle.copy()
    tosave.update(tempdict)

    with open("trello/embed.pickle","wb") as fp:
        pickle.dump(tosave, fp)
    print(f"saved:{tosave}")

class trelloapi(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('trelloapi is ready')

    async def slide_right(self, member):
        pages_json = load_embed()

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

        save_embed(pages_json)
        print("slided right")

    async def slide_left(self, member):
        pages_json = load_embed()

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
        
        save_embed(pages_json)
        print("slided left")

    async def stop(self, member):
        pages_json = load_embed()
        csanel = self.client.get_channel(pages_json[str(member.id)]["channel"])
        msg = await csanel.fetch_message(pages_json[str(member.id)]["message"])
        await msg.delete(delay=None)
        del pages_json[str(member.id)]

        save_embed(tempdict=pages_json)
        print("stop")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        pages_json = load_embed()

        if str(member.id) not in list(pages_json.keys()):
            return

        if(member == self.client.user or member.bot == True):
            return

        #ne lehessen olyat kommentelni, amit a bot nem commentelt

        if payload.emoji.name == "◀️" and msg.id == pages_json[str(member.id)]["message"]:
            await self.slide_left(member)
        elif payload.emoji.name =="🟥" and msg.id == pages_json[str(member.id)]["message"]:
            await self.stop(member)
        elif payload.emoji.name =="▶️" and msg.id == pages_json[str(member.id)]["message"]:
            await self.slide_right(member)

    async def check_embed(self, member):
        pages_json = load_embed()

        if str(member.id) in list(pages_json.keys()):
            csanel = self.client.get_channel(pages_json[str(member.id)]["channel"])
            msg = await csanel.fetch_message(pages_json[str(member.id)]["message"])
            await msg.delete(delay=None)

    @cog_ext.cog_slash(name="login", description="Adatok megadása amivel hozzáférsz a trellohoz", guild_ids=[308599429122883586], options=login_options)
    async def login_slash(self, ctx: SlashContext, api_key,api_secret ,token):
        tokendict = {}
        tempdict={}
        tokendict["token"] = token
        tokendict["api"] = api_key
        tokendict["secret"] = api_secret
        tempdict[str(ctx.author.id)] = tokendict
        save_token(tempdict=tempdict)
        await ctx.send(content="Mentve", hidden=True)

    @cog_ext.cog_slash(name="mytrello", description = "Listázza az általad használt trello boardokat", guild_ids=[308599429122883586], options=None)
    async def mypolls_slash(self, ctx: SlashContext):
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        for count, x in enumerate(all_boards):
            tboard = discord.Embed(
            title = f"Általad használt boardok",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow(),
            url = f"{x.url}")
            tboard.set_thumbnail(url= "https://mpng.subpng.com/20181107/vlx/kisspng-trello-app-store-macos-application-software-ios-5be2bc682da203.7081649815415860241869.jpg")
            tboard.add_field(name="Boardinfo", value=f"Name: {x.name}\nLeírás: {x.description}\nSorszám: {count}/{len(all_boards)-1}", inline=True)
            await ctx.send(embed=tboard, hidden = True)

    @cog_ext.cog_slash(name="createlist", description="Csinál egy listát egy adott boardon", options=list_options)
    async def createlist_slash(self, ctx: SlashContext, boardid=0, listname = "", position=None):
        await ctx.defer(hidden=True)
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        created_list = all_boards[boardid].add_list(name=listname, pos=position)
        await ctx.send(content=f"Created list: {created_list}", hidden=True)
    
    @cog_ext.cog_slash(name="editlist", description="List elemeket tudsz szerkeszteni", options=editlist_options)
    async def editlist_slash(self, ctx: SlashContext, boardid =0, listid = 0, name = None,  position = None, closed = None):
        await ctx.defer(hidden=True)
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        lists = all_boards[boardid].open_lists()
        if position != None:
            lists[listid].move(position=position)
        if closed:
            lists[listid].close()
        if name != None:
            lists[listid].set_name(name=name)
        if name == None and position == None and closed == None:
            await ctx.send(content=":unicorn:")
        else:
            await ctx.send(content="Sikeresen módosítottad a listet", hidden=True)
        print("edited list")

    @cog_ext.cog_slash(name="editcard", description="Card elemeket tudsz szerkeszteni", options=editcard_options)
    async def editcard_slash(self, ctx: SlashContext, boardid = 0, listid = 0, cardid = 0, changelist = None, changepos = None, delete = None, name = None):
        await ctx.defer(hidden=True)
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        lists = all_boards[boardid].open_lists()
        cards = lists[listid].list_cards()
        if changelist != None:
            cards[cardid].change_list(list_id=changelist)
        if changepos != None:
            cards[cardid].change_pos(position=changepos)
        if delete:
            cards[cardid].delete()
        if name != None:
            cards[cardid].set_name(new_name=name)

        if name == None and changelist == None and delete == None and changepos == None:
            await ctx.send(content=":unicorn:")
        else:
            await ctx.send(content="Sikeresen módosítottad a cardot", hidden=True)
        
        print("edited card")

    @cog_ext.cog_slash(name="createcard", description="Csinál egy trello cardot egy adott boardon", options=createcard_options)
    async def createcard_slash(self, ctx: SlashContext, boardid = 0, listid = 0, name = "", description = None, clonefrom = None, position = None):
        await ctx.defer(hidden=True)
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        lists = all_boards[boardid].open_lists()
        created_card = lists[listid].add_card(name=name, desc=description, source=clonefrom, position=position)
        await ctx.send(content=f"Card létrehozva: {created_card}", hidden=True)
        print("card created")

    @cog_ext.cog_slash(name="comment", description="Kommentel egy adott cardhoz", options=comment_options)
    async def comment_slash(self, ctx: SlashContext, comment = "", boardid = 0, listid = 0, cardid = 0):
        await ctx.defer(hidden=True)
        all_boards = get_client(memberid=ctx.author.id).list_boards()
        lists = all_boards[boardid].open_lists()
        cards = lists[listid].list_cards()
        cards[cardid].comment(comment_text=comment)
        await ctx.send(content=f"Kommentáltál ide: {cards[cardid].name}\nEzt: {comment}", hidden=True)
        print("commented")

    @cog_ext.cog_slash(name="lists", description="Kiírja az open listákat egy adott boardon", options=lists_options)
    async def lists_slash(self, ctx: SlashContext, boardid):
        pages_json = {}
        temp_pages = []
        temp_dict = {}

        await ctx.defer()

        #await self.check_embed(ctx.author)

        all_boards = get_client(memberid=ctx.author.id).list_boards()

        members = all_boards[boardid].get_members()

        for lists in all_boards[boardid].open_lists():

            tlist = discord.Embed(
            title = f"List: {lists.name}",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow())

            for count, cards in enumerate(lists.list_cards()):
                labeltxt = ""
                for l in cards._labels:
                    if l.color == "black" or l.color == "white":
                        labeltxt += f"**|** :{l.color}_large_square:__{l.name}__:{l.color}_large_square: "
                    else:
                        labeltxt += f"**|** :{l.color}_square:__{l.name}__:{l.color}_square: "
                labeltxt += "**|**"

                membertxt = ""
                for m in cards.member_id:
                    for mem in members:
                        if m == mem.id:
                            membertxt += f"**|** __{mem.full_name}__ "
                membertxt += "**|**"

                commenttxt = ""
                for c in cards.comments:
                    name = c["memberCreator"]["fullName"]
                    msg = c["data"]["text"]
                    commenttxt += f"\n*{name}* -> {msg}\n"

                tlist.add_field(name=f"__{cards.name}__", value=f"__Sorszám__: {count}\n\n__Leírás__: {cards.desc}\n\n__Label__: {labeltxt}\n\n__Members__: {membertxt}\n\n__Comments__: {commenttxt.rstrip()}\n\n__Url__: <{cards.shortUrl}>", inline=False)
            temp_pages.append(tlist)

        sentmsg = await ctx.send(embed=temp_pages[0])
        #await sentmsg.add_reaction("◀️")
        await sentmsg.add_reaction("🟥")
        await sentmsg.add_reaction("▶️")

        temp_dict["message"] = sentmsg.id
        temp_dict["current"] = 0
        temp_dict["channel"] = ctx.channel.id
        temp_dict["pages"] = temp_pages
        pages_json[str(ctx.author.id)] = temp_dict

        save_embed(tempdict=pages_json)

    @commands.command()
    async def testcog_trelloapi(self, ctx):
        await ctx.send("Cog is ready")   

def setup(client):
    client.add_cog(trelloapi(client))

