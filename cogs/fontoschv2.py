import discord
from discord.ext import commands, tasks

fontos = []

class fontosch(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('fontosch is ready')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        server = self.client.get_guild(payload.guild_id)
        member = await server.fetch_member(payload.user_id)
        csanel = self.client.get_channel(payload.channel_id)
        msg = await csanel.fetch_message(payload.message_id)

        newschannel = self.client.get_channel(752208823867015269)

        if str(payload.emoji) == '❗':
            if csanel == newschannel or msg.id in fontos:
                await msg.clear_reactions()
            else:
                fontos.append(msg.id)
                await newschannel.send(f"{member.mention} szerint ez fontos! ```{msg.content}```Az eredeti üzenet megtekinthető itt:\n{msg.jump_url}")
        elif str(payload.emoji) == '🗑️':
            for x in member.roles:
                if x.name =="admin":
                    await msg.delete(delay = None)

def setup(client):
    client.add_cog(fontosch(client))

