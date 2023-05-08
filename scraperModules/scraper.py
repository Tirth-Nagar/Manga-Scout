import os
import asyncio
import aiohttp
import pymongo
from bs4 import BeautifulSoup
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv

CONNECTION_URL = os.getenv('CONNECTION_URL')

cluster = MongoClient(CONNECTION_URL)
database = cluster["Manga-Update"]
collection = database["User-Data"]

async def getPage(session,url):
    async with session.get(url) as response:
        return await response.text()

async def getAllPages(session,urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(getPage(session,url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results    

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await getAllPages(session,urls)
        return data

def scrape(data):
    newBooks_Dates = {}
    for html in data:
        soup = BeautifulSoup(html, 'html.parser')
        results =  soup.find("img",class_="new-pic")
        if results != None:
            title = soup.find("span",class_="detail-info-right-title-font").text
            updateDate = soup.find("p",class_="title2").text
            newBooks_Dates.update({title:updateDate})
    return newBooks_Dates 

def parse(Books_Dates):
    char = ","
    keyword = "Yesterday"
    updated = []
    for title,date in Books_Dates.items():
        if char not in date or keyword not in date:
            updated.append(title)
    return updated

async def getUpdates(urls):
    html = asyncio.run(main(urls))
    return parse(scrape(html))