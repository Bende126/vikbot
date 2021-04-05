import discord
from discord.ext import commands, tasks
import requests
import json, os
import asyncio
from datetime import datetime

class reaction_roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('idegeschítősch is ready')

    @commands.command()
    async def testcog_rr(self, ctx):
        await ctx.send("Cog is ready")
   
    async def give_role(self, member, guild, emoji):
        """
        roles = await guild.fetch_roles()
        for emotikon in msg.reactions:
            for szerep in roles:
                if(emotikon.name == szerep.name):
                    await member.add_roles(szerep)
        """
        roles = await guild.fetch_roles()
        if emoji.name == "BSS":
            for x in roles:
                if(x.name == emoji.name):
                    addedrole = x
            await member.add_roles(addedrole)
        
        elif emoji.name =="SEM":
            for x in roles:
                if(x.name == emoji.name):
                    addedrole = x
            await member.add_roles(addedrole)

        elif emoji.name == "AC":
            for x in roles:
                if(x.name == emoji.name):
                    addedrole = x
            await member.add_roles(addedrole)

    async def loading(self, channel, msg, delay):
        message = await channel.send(f"{msg} **[**                  **]**")
        await asyncio.sleep(delay)
        await message.edit(content = f"{msg} **[**:white_medium_small_square:            **]**")
        await asyncio.sleep(delay)
        await message.edit(content = f"{msg} **[**:white_medium_small_square::white_medium_small_square:      **]**")
        await asyncio.sleep(delay)
        await message.edit(content = f"{msg} **[**:white_medium_small_square::white_medium_small_square::white_medium_small_square:**]**")
        await asyncio.sleep(delay/2)
        await message.delete(delay = None)

    async def add_message(self, channel, msg_id, guild, links):
        thislist = []
        thisdict = {}

        isdirectory1 = os.path.isdir(f"server_roles\{guild.id}")
        if(isdirectory1 != True):
            os.mkdir(f"server_roles\{guild.id}")
            message = f"Creating dictionary directory for guild: {guild.name}"
            await self.loading(channel, message, 3)

        isdirectory2 = os.path.isdir(f"server_roles\{guild.id}\messages")
        if(isdirectory2 != True):
            os.mkdir(f"server_roles\{guild.id}\messages")
            message = f"Creating messages directory for guild: {guild.name}"
            await self.loading(channel, message, 4)

        isfile1 = os.path.isfile(f"server_roles\{guild.id}\messages\{msg_id}.json")
        if(isfile1 != True):
            f = open(f"server_roles\{guild.id}\messages\{msg_id}.json", "x")
            f.close()

        isfile2 = os.path.isfile(f"server_roles\{guild.id}\messages.txt")
        if(isfile2 != True):
            f = open(f"server_roles\{guild.id}\messages.txt", "x")
            f.close()

        f = open(f"server_roles\{guild.id}\messages.txt", "r")
        readfile = f.readlines()
        for x in readfile:
            thislist.append(int(x[:-1]))
        f.close()

        thisdict["message id"] = msg_id
        thisdict["link integer"] = links

        f = open(f"server_roles\{guild.id}\messages\{msg_id}.json", "w")
        json.dump(thisdict, f)
        f.close()

        for x in thislist:
            if(x == msg_id):
                await channel.send("Message data has been rewritten.")
                return
                
        thislist.append(msg_id)
        
        f = open(f"server_roles\{guild.id}\messages.txt", "wt")
        for x in thislist:
            f.write(f"{x}\n")
        f.close()

        await channel.send("Message added to the dictionary.")

    async def add_emoji(self, emoji, role, channel, guild):
        thisdict = {}
        oldid = None
        
        isdirectory1 = os.path.isdir(f"server_roles\{guild.id}")
        if(isdirectory1 != True):
            os.mkdir(f"server_roles\{guild.id}")
            message = f"Creating dictionary directory for guild: {guild.name}"
            await self.loading(channel, message, 3)

        isdirectory2 = os.path.isdir(f"server_roles\{guild.id}\links")
        if(isdirectory2 != True):
            os.mkdir(f"server_roles\{guild.id}\links")
            message = f"Creating emoji-role directory for guild: {guild.name}"
            await self.loading(channel, message, 3)

        isfile1 = os.path.isfile(f"server_roles\{guild.id}\links\{emoji.id}.json")
        if(isfile1 != True):
            f = open(f"server_roles\{guild.id}\links\{emoji.id}.json", "x")
            f.close()
            thisdict["ID"] = len(os.listdir(f"server_roles\{guild.id}\links"))
        else:
            f = open(f"server_roles\{guild.id}\links\{emoji.id}.json")
            oldid = json.loads(f.read())
            thisdict["ID"] = int(oldid["ID"])
            f.close()
        
        thisdict["emoji_id"] = emoji.id
        thisdict["role_id"] = role.id

        f = open(f"server_roles\{guild.id}\links\{emoji.id}.json", "w")
        json.dump(thisdict, f)
        f.close()
        if(oldid == None):
            await channel.send("Emoji-role link succesfully created.")
        else:
            await channel.send("Emoji-role link succesfully overwritten.")

    async def remove_message(self, msg_id, guild, channel):
        thislist = []
        
        isfile = os.path.isfile(f"server_roles\{guild.id}\messages.txt")
        if(isfile != True):
            await channel.send("This message is not saved as reaction role message")
            return

        f = open(f"server_roles\{guild.id}\messages.txt", "r")
        readfile = f.readlines()
        for x in readfile:
            thislist.append(int(x[:-1]))
        f.close()
        thislist.remove(msg_id)
        os.remove(f"server_roles\{guild.id}\messages\{msg_id}.json")
        f = open(f"server_roles\{guild.id}\messages.txt", "wt")
        for x in thislist:
            f.write(f"{x}\n")
        f.close()
        message = "Removing message from dictionary."
        await self.loading(channel, message, 3)

    async def remove_emoji(self, emoji, guild, channel):
        isfile = os.path.isfile(f"server_roles\{guild.id}\links\{emoji.id}.json")
        if(isfile != True):
            await channel.send("There is no role linked to this emoji.")
            return

        
        readfile = json.loads(open(f"server_roles\{guild.id}\links\{emoji.id}.json"))

        files = os.listdir

        for x in files:
            f = open(f"server_roles\{guild.id}\links\{x}")
            

        os.remove(f"server_roles\{guild.id}\links\{emoji.id}.json")
        await channel.send("Emoji is no longer linked to role.")

    @commands.group(brief = "add <message/link>")
    async def add(self, ctx):
        if(ctx.invoked_subcommand == None):
            await ctx.send("Többrészes parancs és nem látom a folytatást")

    @add.command()
    async def message(self, ctx, id: int, link_ids: int = 0):
        await self.add_message(ctx.channel, id, ctx.guild, link_ids)

    @add.command(description = "set_emoji <custom emoji> <mentioned role>")
    async def link(self, ctx, emoji: discord.Emoji, role: discord.Role):
        await self.add_emoji(emoji, role, ctx.channel, ctx.guild)

    @commands.group(brief = "remove <message/emoji>")
    async def remove(self, ctx):
        if(ctx.invoked_subcommand == None):
            await ctx.send("Többrészes parancs és nem látom a folytatást")

    @remove.command()
    async def message(self, ctx, id: int):
        await self.remove_message(id, ctx.guild, ctx.channel)

    @remove.command()
    async def emoji(self, ctx, emoji: discord.Emoji):
        await self.remove_emoji(emoji, ctx.guild, ctx.channel)

    @commands.command()
    async def list_links(self, ctx):
        isdir = os.path.isdir(f"server_roles\{ctx.guild.id}\links")
        if(isdir != True):
            await ctx.send(f"There is no database for this guild: {ctx.guild.name}.")
            return
        files = os.listdir(f"server_roles\{ctx.guild.id}\links")
        if(len(files) == 0):
            await ctx.send(f"There is no emoji-role link in this guild: {ctx.guild.name}")
            return
        emojis = ctx.guild.emojis
        roles = await ctx.guild.fetch_roles()

        embed = discord.Embed(
            title = "The created links between emojis and roles",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url= self.client.user.avatar_url)
        
        for x in files:
            f = open(f"server_roles\{ctx.guild.id}\links\{x}", "r")
            thisdict = json.loads(f.read())
            f.close()
            for emoji in emojis:
                if(emoji.id == thisdict["emoji_id"]):
                    addedemoji = emoji
            for role in roles:
                if(role.id == thisdict["role_id"]):
                    addedrole = role
            embed.add_field(name = f"ID:{thisdict['ID']}", value = f"{addedemoji} -> {addedrole.mention}", inline = False)

        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        if(member == self.client.user or member.bot == True):
            return

        print(msg.content)

def setup(client):
    client.add_cog(reaction_roles(client))

