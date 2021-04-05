import re
import os
import discord
import feedparser
from discord.ext import commands, tasks
from discord import Webhook, RequestsWebhookAdapter
import requests

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
        
    @tasks.loop(seconds=10)
    async def loops(self):
        print('loop')
        global sources
        for source in sources:
            news_list = get_news(sources[source])
            for news in get_unseen(news_list, source):
                print(news)
                seen_news(news_list, source)
                embed = discord.Embed(
                    title = news_list[0].title,
                    url = news_list[0].url,
                    colour = discord.Colour.blue()
                    )
                embed.add_field(name='Leírás: ', value=news_list[0].descr, inline=True)
                embed.set_thumbnail(url= self.client.user.avatar_url)
                embed.set_footer(text=news_list[0].date[:-9])
                csanel = self.client.get_channel(739557734705397812)    #787045110168813598(announcement) 739557734705397812(viknews)
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
    seen_file = open('seen_'+source+'.txt', 'w')
    for news in news_list:
        seen_file.write(news.date+'\n')
    seen_file.close()

def get_unseen(news_list, source):
    unseen = []
    if not os.path.isfile('seen_'+source+'.txt'):
        return unseen
    seen_file = open('seen_'+source+'.txt')
    seen = [line.strip() for line in seen_file.readlines()]
    for news in news_list:
        if news.date not in seen:
            unseen.append(news)
    seen_file.close()
    return unseen
