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
        print('reactionrole is ready')

    @commands.command()
    async def testcog_rr(self, ctx):
        await ctx.send("Cog is ready")

    def check_file(self, path):
        return os.path.isfile(path)

    def create_file(self, path):
        isfile = os.path.isfile(path)
        if(isfile != True):
            f = open(path, "x")
            f.close()
        return

    def read_file(self, path):
        with open(path, "r") as fp:
            return fp.read()
        
    def write_file(self, path, content):
       f = open(path, "w")
       json.dump(content, f)
       f.close()
       return

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
    
    async def check_directory(self, guild, channel, path):
        isdir = os.path.isdir(path)
        if(isdir != True):
            os.mkdir(path)
            await self.loading(channel, f"Creating dictionary directory for guild: {guild.name}", 2)
        return

    async def add_message(self, channel, msg_id, guild, links):
        thislist = []
        thisdict = {}

        await self.check_directory(guild, channel, f"server_roles\{guild.id}")

        await self.check_directory(guild, channel, f"server_roles\{guild.id}\messages")

        self.create_file(f"server_roles\{guild.id}\messages\{msg_id}.json")

        self.create_file(f"server_roles\{guild.id}\messages.txt")

        readfile = self.read_file(f"server_roles\{guild.id}\messages.txt")

        for x in readfile:
            thislist.append(int(x[:-1]))

        thisdict["message id"] = msg_id
        thisdict["link integer"] = links

        self.write_file(f"server_roles\{guild.id}\messages\{msg_id}.json", thisdict)

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

        await self.check_directory(guild, channel, f"server_roles\{guild.id}")

        await self.check_directory(guild, channel, f"server_roles\{guild.id}\links")

        self.create_file(f"server_roles\{guild.id}\links\{emoji.id}.json")

        thisdict["ID"] = len(os.listdir(f"server_roles\{guild.id}\links"))

        oldid = json.loads(self.read_file(f"server_roles\{guild.id}\links\{emoji.id}.json"))
        thisdict["ID"] = int(oldid["ID"])
        
        thisdict["emoji_id"] = emoji.id
        thisdict["role_id"] = role.id

        self.write_file(f"server_roles\{guild.id}\links\{emoji.id}.json", thisdict)

        if(oldid == None):
            await channel.send("Emoji-role link succesfully created.")
        else:
            await channel.send("Emoji-role link succesfully overwritten.")

    async def remove_message(self, msg_id, guild, channel):
        thislist = []

        if(self.check_file(f"server_roles\{guild.id}\messages.txt") != True):
            await channel.send(f"There is no dictionary for this guild: {guild.name}")
            return

        readfile = self.read_file(f"server_roles\{guild.id}\messages.txt")
        for x in readfile:
            thislist.append(int(x[:-1]))

        thislist.remove(msg_id)
        os.remove(f"server_roles\{guild.id}\messages\{msg_id}.json")
        
        f = open(f"server_roles\{guild.id}\messages.txt", "wt")
        for x in thislist:
            f.write(f"{x}\n")
        f.close()

        await self.loading(channel, "Removing message from dictionary.", 3)

    async def remove_emoji(self, emoji, guild, channel):
        if(self.check_file(f"server_roles\{guild.id}\links\{emoji.id}.json") != True):
            await channel.send("There is no role linked to this emoji.")
            return

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
            thisdict = json.loads((self.read_file(f"server_roles\{ctx.guild.id}\links\{x}")))
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

