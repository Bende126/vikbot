import discord 
from discord.ext import commands, tasks
import time, os
from itertools import cycle

prefixes = ['.', ',', '!!', 'xd']

async def get_prefix(client, message):
    if not message.guild:
        return
    return commands.when_mentioned_or(*prefixes)(client, message)

client = commands.Bot(command_prefix = get_prefix, status = discord.Status.idle, activity=discord.Game(name="Booting.."))
status = cycle(['Rossz csatorna', 'E M B E R', 'Literálisan cringe'])
 #botspam, admin botspam
channelids =[739567794533826616, 745624827368570930]

@client.event
async def on_ready():
		print('Lets rock!')
		print(client.user.name)
		print(client.user.id)
		print("----------")
		await client.change_presence(status=discord.Status.online, activity=discord.Game(name="with fire"))

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel.id in channelids or message.author.id == 297689894208274432:
            await client.process_commands(message)
        elif message.content[0] in prefixes:
            await message.author.send(next(status))

@client.command(brief = 'Prefix hozzáadása')
async def add_prefix(ctx, prefix):
    global prefixes
    if prefix in prefixes:
        await ctx.channel.send('Már létezik, te literális majom! :rofl:')
    else:
        prefixes.append(prefix)
        await ctx.channel.send(f'Added `{prefix}` to the prefix list. :ok_hand:')

@client.command(brief = 'Prefix eltávolítása')
async def remove_prefix(ctx, prefix):
    if prefix in prefixes:
        prefixes.remove(prefix)
        await ctx.channel.send(f'Removed `{prefix}` from the prefix list.')
    else:
        await ctx.channel.send('Nincs ilyen prefix! :angry::anger:')

@client.command(brief = 'Prefixek listája")
async def prefixlist(ctx):
    msgs = '['
    msg = ''
    for x in prefixes:
        msg = msg+ msgs+ x+'] '
    await ctx.channel.send(f'```{msg}```')


@client.command(brief='Betölti az összes cogot.')
async def loadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.command(brief='Betölti a cogot fájlnév szerint.')
async def loadcog(ctx, cogfilename):
    client.load_extension(f"cogs.{cogfilename}")
    await ctx.channel.send(f'Cog {cogfilename} loaded')

@client.command(brief='Megszűnteti a cog használatát fájlnév szerint.')
async def unloadcog(ctx, cogfilename):
    client.unload_extension(f"cogs.{cogfilename}")
    await ctx.channel.send(f'Cog {cogfilename} unloaded')

@client.command(brief='Cognevek listája fájlnév szerint.')
async def coglist(ctx):
    lista = ''
    for x in os.listdir('./cogs'):
        if x.endswith('.py'):
            lista = lista+(x[:-3])
    await ctx.channel.send(lista)
        
@client.command(hidden = True)
async def kys(ctx):
    if ctx.author.id == 297689894208274432:
        await ctx.channel.send("Going back to vietnam")
        await client.logout()
        exit()
    else:
        await ctx.channel.send("Te nem sorozhatsz be! :stuck_out_tongue_closed_eyes:")

client.run("")


