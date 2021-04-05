import discord
from discord.ext import commands, tasks
import os
from sympy import *
from PIL import Image, ImageDraw, ImageFont

prefixes = ['szgabi', '+']

def makeimg(txt):
    filename = "img.png"
    image = Image.new(mode = "RGB", size = (len(txt)*14+6, 50), color = "white")
    fnt = ImageFont.truetype('arial.ttf', 30)
    draw = ImageDraw.Draw(image)
    draw.text((1,5), txt.replace('**','^'), font=fnt, fill=(0,0,0))

    image.save(filename)
    return filename

async def get_prefix(client, message):
    if not message.guild:
        return
    return commands.when_mentioned_or(*prefixes)(client, message)

client = commands.Bot(command_prefix = get_prefix, status = discord.Status.idle, activity=discord.Game(name="Booting.."))

@client.event
async def on_ready():
		print('Lets rock!')
		print(client.user.name)
		print(client.user.id)
		print(client.guilds)
		print("----------")
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="students cry"))

"""
for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            """

@client.event
async def on_message(message):
    print(f'{message.content}')
    await client.process_commands(message)
    
@client.command(description='Kills the bot')
async def kys(ctx):
    if ctx.author.id == 297689894208274432:
        await ctx.channel.send("T Ö :regional_indicator_r: T É N E T E S E N")
        await client.logout()
        exit()
    else: await ctx.channel.send("You jerk!")

@client.command()
async def iintegral(ctx, fv, dt):
    x = Symbol(dt)
    summa = integrate(fv,x)
    await ctx.send("A kapott eredmény történetesen:")
    await ctx.channel.send(file=discord.File(f'{makeimg(str(summa))}'))

@client.command()
async def integral(ctx, fv, dt, a, b):
    x = Symbol(dt)
    summa = integrate(fv, (x, a, b))
    summma = integrate(fv, x)
    await ctx.send("A határozatlan integrálja:")
    await ctx.channel.send(file=discord.File(f'{makeimg(str(summma))}'))
    await ctx.send("A kapott eredmény történetesen:")
    await ctx.channel.send(file=discord.File(f'{makeimg(str(summa))}'))

@client.command()
async def derival(ctx, fv, dt, number):
    x = Symbol(dt)
    summa = diff(fv, x, number)
    await ctx.send("A kapott eredmény történetesen:")
    await ctx.channel.send(file=discord.File(f'{makeimg(str(summa))}'))

@client.command()
async def limes(ctx, fv, a, b):
    summa = limit(fv, a, b)
    await ctx.send("A kapott eredmény történetesen:")
    await ctx.channel.send(file=discord.File(f'{makeimg(str(summa))}'))

@client.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command(description ='Asks for server latency')
async def ping(ctx):
	ping_ = client.latency
	ping = round(ping_ *1000)
	await ctx.channel.send(f"Késik a kép drága? Csakis ennyit késhet {ping}ms")

@client.group()
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command passed...')

@prefix.command()
async def add(ctx, prefix):
    global prefixes
    if prefix in prefixes:
        await ctx.channel.send('Már létezik, te literális majom! :rofl:')
    else:
        prefixes.append(prefix)
        await ctx.channel.send(f'Added `{prefix}` to the prefix list. :ok_hand:')

@prefix.command()
async def remove(ctx, prefix):
    if prefix in prefixes:
        prefixes.remove(prefix)
        await ctx.channel.send(f'Removed `{prefix}` from the prefix list.')
    else:
        await ctx.channel.send('Nincs ilyen prefix! :angry::anger:')

@prefix.command()
async def list(ctx):
    msgs = '['
    msg = ''
    for x in prefixes:
        msg = msg+ msgs+ x+'] '
    await ctx.channel.send(f'```{msg}```')

client.run("")

