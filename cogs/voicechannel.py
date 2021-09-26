import discord
from discord.ext import commands
from datetime import datetime

from discord.ext.commands.errors import NoEntryPointError

class voicechannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('voicechannel is ready')

    @commands.command()
    async def testcog_voicechannel(self, ctx):
        await ctx.send("Cog is ready")

    @commands.command()
    async def set_parent_channel(self, ctx, id: int = 0):
        global parentid
        if(id ==0):
            await ctx.send("Az id nem lehet 0")
            return
        with open("voicechannel/parentchannelids.txt", 'a') as fp:
            fp.write(f"{id}\n")

    @commands.command()
    async def get_parent_channels(self,ctx):

        with open("voicechannel/parentchannelids.txt", "r") as fp:
            lines = fp.readlines()

        embed = discord.Embed(
            title = "Parental voicechannels",
            colour = discord.Colour.blue(),
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url= self.client.user.avatar_url)
        for x in lines:
            if(x==None):
                return
            ch = self.client.get_channel(int(x))
            embed.add_field(name=ch.name, value=f"Guild: {ch.guild}\n Category: {ch.category}\n Position: {ch.position}")

        await ctx.send(embed = embed)

    @commands.command()
    async def remove_parent_channel(self, ctx, id: int):
        with open("voicechannel/parentchannelids.txt", "r") as fp:
            lines = fp.readlines()
        with open("voicechannel/parentchannelids.txt", "w") as fp:
            for line in lines:
                if line.strip("\n") != f"{id}":
                    fp.write(line)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if(member.bot == True):
            return
        
        with open("voicechannel/parentchannelids.txt", 'r') as fp:
            parentids = fp.read()

        #ha belép a szobát szeretnékbe
        if(after.channel !=None and str(after.channel.id) in parentids):
            print("joined to parent channel")

            channelname = member.nick
            if member.nick == None:
                channelname = member.name
            channel = await member.guild.create_voice_channel(f"{channelname} által kért voice")
            await channel.edit(position=after.channel.position+1, category=after.channel.category, sync_permissions=True)
            await channel.set_permissions(member, manage_channels=True)
            await member.move_to(channel)

            with open("voicechannel/channelids.txt", 'a') as fp:
                fp.write(f"{channel.id}\n")

        # ha lelép a kapott szobából
        if(before.channel != None and after.channel == None):
            with open("voicechannel/channelids.txt", 'r') as fp:
                content = fp.read()
            if(len(before.channel.members)==0 and str(before.channel.id) in content):
                await before.channel.delete()

                with open("voicechannel/channelids.txt", "r") as fp:
                    lines = fp.readlines()
                with open("voicechannel/channelids.txt", "w") as fp:
                    for line in lines:
                        if line.strip("\n") != f"{before.channel.id}":
                            fp.write(line)

        #ha ellép a kapott szobából
        if(before.channel != None and after.channel != None):
            with open("voicechannel/channelids.txt", 'r') as fp:
                content = fp.read()
            if(len(before.channel.members)==0 and str(before.channel.id) in content):
                await before.channel.delete()

                with open("voicechannel/channelids.txt", "r") as fp:
                    lines = fp.readlines()
                with open("voicechannel/channelids.txt", "w") as fp:
                    for line in lines:
                        if line.strip("\n") != f"{before.channel.id}":
                            fp.write(line)


def setup(client):
    client.add_cog(voicechannel(client))

