import discord
from discord.ext import commands, tasks
import urllib.request
from lxml import html
import time, random, asyncio
from datetime import date, datetime

class News:
    def __init__(self, title, date, url, descr):
        self.title = title
        self.date = date
        self.url = 'https://www.vik.bme.hu' + url
        self.descr = descr

    def __str__(self):
        return '''{{
  title: {}
  date: {}
  url: {}
  descr: {}
}}'''.format(self.title, self.date, self.url, self.descr)

    def __repr__(self):
        return str(self)


last_news = None
news = []
args = ['B A S E D', 'test', 'ok boomer', 'mifaszomatírjakidee', ':heart:', ':dab:' ]
bounds = {}

class viknews(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('vik.bme.hu is ready')
        self.loops.start()
        
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
                await y.send(f'If you received `{args[rnd]}` then it\'s working!')

    @commands.command(brief = 'Linkeli a botot a csatornához')
    async def bound(self, ctx):
        csanel = ctx.channel
        server = ctx.guild
        bounds[csanel.name] = csanel

    @tasks.loop(seconds=5)
    async def loops(self):
        global news_list
        global last_news
        
        news_list = getnews()
        if last_news == None:
            last_news = news_list[0]
        elif str(last_news) == str(news_list[0]):
            return
        last_news = news_list[0]
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_footer(text=news_list[0].date)
        if bounds == {}:
            return
        else:
            for x in bounds.values():
                await x.send(embed=embed)

    @commands.command(brief = 'Hírek lekérése a vik.bme.huról.')
    async def viknews(self, ctx):
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_footer(text=news_list[0].date)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(viknews(client))

def convdate(str_date):
    trans_dict = {'január': 'January', 'február': 'February', 'március': 'March', 'április': 'April', 'május': 'May', 'június': 'June', 'július': 'July', 'augusztus': 'August', 'szeptember': 'September'} # todo befejezni
    split_date = str_date.split()
    trans_date = split_date[:1] + [trans_dict[split_date[1]]] + split_date[2:3]
    return datetime.strptime(' '.join(trans_date), '%Y. %B %d.')

def getnews():
    news = []
    
    fp = urllib.request.urlopen('http://www.vik.bme.hu/hirek')
    mybytes = fp.read()
    mystr = mybytes.decode('utf8')
    fp.close()
    
    tree = html.fromstring(mybytes)
    dates = tree.find_class('date')
    titles = tree.find_class('title')
    urls = tree.xpath('.//div[@class=\'news-item\']/p/a/@href')
    des = tree.find_class('description')

    for i in range(len(titles)):
        news.append(News(titles[i].text_content(), convdate(dates[i].text_content()), urls[i], des[i].text_content().strip()))

    news.sort(key=lambda n: n.date, reverse=True)
    return news

news_list = getnews()
last_news = news_list[0]
print(news_list[:2])
