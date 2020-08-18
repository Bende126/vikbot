import discord
from discord.ext import commands, tasks
import urllib.request
from lxml import html
import time, random, asyncio

newstitles = []
dates = []
rom = []
url = []
args = ["B A S E D", "test", "ok boomer", "mifaszomatírjakidee", ":heart:", ":dab:" ]

bounds = {}

class viknews(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loops.start()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('vik.bme.hu is ready')
        
    @commands.command(brief = 'Default cogtest')
    async def viknews_test(self, ctx):
        await ctx.channel.send('Cog is loaded')

    @commands.command(brief = 'Bounded channel testing')
    async def bound_test(self, ctx):
        rnd = random.randint(0, 5)
        if bounds == {}:
            await ctx.channel.send('No bounds yet! :rage:')
        else:
            for x in bounds.values():
                await x.send(args[rnd])
            await asyncio.sleep(5)
            for y in bounds.values():
                await y.send(f"If you received `{args[rnd]}` then it's working!")

    @commands.command(brief = 'Linkeli a botot a csatornához')
    async def bound(self, ctx):
        csanel = ctx.channel
        server = ctx.guild
        bounds[csanel.name] = csanel

    @tasks.loop(seconds=60)
    async def loops(self):
        global rom
        dates.clear()
        getnews()
        if rom == dates:
            return
        else: print("News: ")
        rom = dates.copy()
        embed = discord.Embed(
            title = newstitles[0],
            url = realurl,
            colour = discord.Colour.blue()
            )
        embed.set_footer(text=dates[0])
        if bounds == {}:
            return
        else:
            for x in bounds.values():
                await x.send(embed=embed)

    @loops.before_loop
    async def before_loops(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @commands.command(brief = 'Hírek lekérése a vik.bme.huról.')
    async def viknews(self, ctx):
        realurl = ("https://www.vik.bme.hu" + url[0])
        embed = discord.Embed(
            title = newstitles[0],
            url = realurl,
            colour = discord.Colour.blue()
            )
        embed.set_footer(text=dates[0])
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(viknews(client))

def getnews():
    global newstitles
    global dates
    global url
    
    fp = urllib.request.urlopen("http://www.vik.bme.hu/hirek")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    tree = html.fromstring(mybytes)
    dateshtml = tree.find_class('date')
    title = tree.find_class('title')
    url = tree.xpath(".//div[@class='news-item']/p/a/@href")

    for i in range(0, len(title)):
        newstitles.append(title[i].text_content())
    for i in range(0, len(dateshtml)):
        dates.append(dateshtml[i].text_content())

getnews()
rom = dates.copy()
print(rom)
