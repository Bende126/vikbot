import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

fontos = []

class fontosch(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.polls = []
        self.scheduler = AsyncIOScheduler()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('fontosch is ready')
        self.scheduler.start()

    @commands.command()
    async def testcog_fontosch(self, ctx):
        await ctx.send("Cog is ready")

    async def remove_role(self, user, role):
        await user.remove_roles(role)
        print(f"Removed {role.name} role to {user.name}")
    
    async def complete_poll(self, channel_id, message_id, ember ,guild):
        message = await self.client.get_channel(channel_id).fetch_message(message_id)

        most_voted = max(message.reactions, key=lambda r: r.count)

        if most_voted.emoji == "✅":
            await message.channel.send(f" A szavazás lezárva! {ember.mention} hivatalosan is idegeschítő!")
            roles = await guild.fetch_roles()
            for x in roles:
                if x.name == "idegeschítő":
                    addedrole = x
            await ember.add_roles(addedrole)
            print(f"Added {addedrole.name} role to {ember.name}")
            self.scheduler.add_job(self.remove_role, "date", run_date=datetime.utcnow()+timedelta(seconds=3600), args=[ember, addedrole])

        else:
            await message.channel.send(f"Megúsztad {ember.mention}, legközelebb nem így lesz!")
        #await message.channel.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")

        self.polls.remove((message.channel.id, message.id))

    @commands.command(brief = "<command> <user mention> <minutes>")
    async def createpoll(self, ctx, user, mins: int):
        embed = discord.Embed(title="The trial commences",
					  colour=ctx.author.colour,
					  timestamp=datetime.utcnow()
                      )
        if ctx.message.mentions[0] == self.client.user and len(ctx.message.mentions) >= 2:
            boomer = ctx.message.mentions[1]
        else:
            boomer = ctx.message.mentions[0]

        embed.add_field(name = "Szavazz!", value = f"Idegeschítő-e {user}?\n✅ igen\n❌ nem", inline=False)
        dates = datetime.utcnow()+timedelta(seconds=3600+mins*60)
        embed.add_field(name = "Ekkor van vége:", value = f"{str(dates)[:-7]} UTC", inline=False)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        self.polls.append((message.channel.id, message.id))

        print(datetime.utcnow())
        print(f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC")

        self.scheduler.add_job(self.complete_poll, "date", run_date=datetime.utcnow()+timedelta(seconds=mins*60), args=[message.channel.id, message.id, boomer, ctx.guild])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        if payload.message_id in (poll[1] for poll in self.polls):
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            
            for reaction in message.reactions:
                if (not payload.member.bot and payload.member in await reaction.users().flatten() and reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)

        if payload.emoji.name == 'torlosch':
            for x in member.roles:
                if x.name =="admin":
                    await msg.delete(delay = None)
        
        elif payload.emoji.name == 'announcement':
            for x in member.roles:
                if x.name =="admin":
                    await msg.publish()

def setup(client):
    client.add_cog(fontosch(client))


