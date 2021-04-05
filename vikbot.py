import discord 
from discord.ext import commands, tasks
import os
from itertools import cycle
from discord_slash import SlashCommand, SlashCommandOptionType

prefixes = ['.', ',']

async def get_prefix(client, message):
    if not message.guild:
        return
    return commands.when_mentioned_or(*prefixes)(client, message)
intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, status = discord.Status.idle, activity=discord.Game(name="Booting.."))
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload = True)

#botspam
channelids =[739567794533826616]


@client.event
async def on_ready():
		print('Lets rock!')
		print(client.user.name)
		print(client.user.id)
		print("----------")
		#await client.change_presence(status=discord.Status.online, activity=discord.Game(name="with fire"))
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="@vikbot"))

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel.id in channelids or message.author.id ==297689894208274432 or message.guild.id ==750411287095279669:
            await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@client.command(brief = "Lekéri a pinget")
async def ping(ctx):
    await ctx.send(f'A késés változója: {round(client.latency*1000)}ms')

@client.group(brief = 'Prefix maincommand')
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Többrészes parancs és nem látom a folytatást...')

@prefix.command(brief = 'Prefix hozzáadása')
async def add(ctx, prefix):
    global prefixes
    if prefix in prefixes:
        await ctx.channel.send('Már létezik, te literális majom! :rofl:')
    else:
        prefixes.append(prefix)
        await ctx.channel.send(f'Added `{prefix}` to the prefix list. :ok_hand:')

@prefix.command(brief = 'Prefix eltávolítása')
async def remove(ctx, prefix):
    if prefix in prefixes:
        prefixes.remove(prefix)
        await ctx.channel.send(f'Removed `{prefix}` from the prefix list.')
    else:
        await ctx.channel.send('Nincs ilyen prefix! :angry::anger:')

@prefix.command(brief = 'Prefixek listája')
async def list(ctx):
    msgs = '['
    msg = ''
    for x in prefixes:
        msg = msg+ msgs+ x+'] '
    await ctx.channel.send(f'```{msg}```')

@client.group(brief = 'Cog maincommand')
async def cog(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Többrészes parancs és nem látom a folytatást...')

@cog.command(brief='Betölti az összes cogot.')
async def loadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@cog.command(brief='Betölti a cogot fájlnév szerint.')
async def load(ctx, cogfilename):
    client.load_extension(f"cogs.{cogfilename}")
    await ctx.channel.send(f'Cog {cogfilename} loaded')

@cog.command(brief='Megszűnteti a cog használatát fájlnév szerint.')
async def unload(ctx, cogfilename):
    client.unload_extension(f"cogs.{cogfilename}")
    await ctx.channel.send(f'Cog {cogfilename} unloaded')

@cog.command(brief='Cognevek listája fájlnév szerint.')
async def list(ctx):
    lista = '```'
    for x in os.listdir('./cogs'):
        if x.endswith('.py'):
            lista = lista + x[:-3] + " "
    lista += "```"
    await ctx.channel.send(lista)
        
@client.command(hidden = True)
async def kys(ctx):
    if ctx.author.id == 297689894208274432:
        await ctx.channel.send("Going back to vietnam")
        await client.close()
        exit()
    else:
        await ctx.channel.send("Te nem sorozhatsz be! :stuck_out_tongue_closed_eyes:")

client.run("")


