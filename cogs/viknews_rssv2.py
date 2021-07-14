import re
import os
import discord
import feedparser
from discord.ext import commands, tasks
from datetime import datetime

class News:
    def __init__(self, title, date, url, descr):
        self.title = title
        self.date = date
        self.url = url
        self.descr = descr

    def __str__(self):
        return '''{{
  title: {}
  date: {}
  url: {}
  descr: {}
}}'''.format(self.title, self.date[:-9], self.url, self.descr)

    def __repr__(self):
        return str(self)

sources = {'vik': 'https://vik.bme.hu/rss/', 'kth': 'https://kth.bme.hu/rss/'}

class viknews_by_BoA(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('vik.bme.hu is ready')
        self.loops.start()
        
    @tasks.loop(seconds=60)
    async def loops(self):
        print('loop')
        global sources
        for source in sources:
            news_list = get_news(sources[source])
            for index, news in enumerate(get_unseen(news_list, source)):
                print(news)
                seen_news(news_list, source)
                embed = discord.Embed(
                    title = news_list[index].title,
                    url = news_list[index].url,
                    colour = discord.Colour.blue()
                    )
                embed.add_field(name='Leírás: ', value=news_list[index].descr, inline=True)
                embed.set_thumbnail(url= self.client.user.avatar_url)
                embed.set_footer(text=news_list[index].date[:-9])

                with open("viknews/newschannelids.txt", "r") as fp:
                    lines = fp.readlines()
                for x in lines:
                    if(x==None):
                        return
                    csanel = self.client.get_channel(int(x))    #787045110168813598(announcement) 739557734705397812(viknews)
                    await csanel.send(embed =embed)

    @commands.command(brief = 'Hírek lekérése a vik.bme.huról.')
    async def viknews(self, ctx):
        global sources
        news_list = get_news(sources['vik'])
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_thumbnail(url= self.client.user.avatar_url)
        embed.set_footer(text=news_list[0].date[:-9])
        await ctx.channel.send(embed=embed)

    @commands.command(brief = 'Hírek lekérése a kth.bme.huról.')
    async def kthnews(self, ctx):
        global sources
        news_list = get_news(sources['kth'])
        embed = discord.Embed(
            title = news_list[0].title,
            url = news_list[0].url,
            colour = discord.Colour.blue()
            )
        embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
        embed.set_thumbnail(url= self.client.user.avatar_url)
        embed.set_footer(text=news_list[0].date[:-9])
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def set_news_channel(self, ctx, id: int = 0):
        global parentid
        if(id ==0):
            await ctx.send("Az id nem lehet 0")
            return
        with open("viknews/newschannelids.txt", 'a') as fp:
            fp.write(f"{id}\n")

    @commands.command()
    async def get_news_channels(self,ctx):

        with open("viknews/newschannelids.txt", "r") as fp:
            lines = fp.readlines()

        embed = discord.Embed(
            title = "News-channels",
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
    async def remove_news_channel(self, ctx, id: int):
        with open("viknews/newschannelids.txt", "r") as fp:
            lines = fp.readlines()
        with open("viknews/newschannelids.txt", "w") as fp:
            for line in lines:
                if line.strip("\n") != f"{id}":
                    fp.write(line)

def setup(client):
    client.add_cog(viknews_by_BoA(client))

def get_news(url):
    clean = re.compile('<.*?>')
    news = []
    feed = feedparser.parse(url)
    for news_item in feed['entries']:
        news.append(News(news_item.title, news_item.published, news_item.link, re.sub(clean, '', news_item.summary)))
    return news

def seen_news(news_list, source):
    seen_file = open('viknews/seen_'+source+'.txt', 'w')
    for news in news_list:
        seen_file.write(news.date+'\n')
    seen_file.close()

def get_unseen(news_list, source):
    unseen = []
    if not os.path.isfile('viknews/seen_'+source+'.txt'):
        return unseen
    seen_file = open('viknews/seen_'+source+'.txt')
    seen = [line.strip() for line in seen_file.readlines()]
    for news in news_list:
        if news.date not in seen:
            unseen.append(news)
    seen_file.close()
    return unseen
