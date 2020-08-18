import discord 
from discord.ext import commands, tasks
import time, os

client = commands.Bot(command_prefix = '!', status = discord.Status.idle, activity=discord.Game(name="Booting.."))

@client.event
async def on_ready():
		print('Lets rock!')
		print(client.user.name)
		print(client.user.id)
		print(client.guilds)
		print("----------")
		await client.change_presence(status=discord.Status.online, activity=discord.Game(name="with fire"))

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_message(message):
    await client.process_commands(message)

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
    else: await ctx.channel.send("You jerk!")

client.run("")


