import os
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

def getUrls(titles):
    baseUrl = "http://fanfox.net/manga/"
    formatTitle = lambda title : title.casefold().replace(" ", "_").replace(":", "").replace("!", "").replace("?", "").replace("'", "_").replace("(","").replace(")","").replace(",","").replace(".","").replace("-","_")
    return [baseUrl+formatTitle(title) for title in titles]

load_dotenv()

DISCORD_TOKEN  = os.getenv('DISCORD_TOKEN')
CONNECTION_URL = os.getenv('CONNECTION_URL')

intents = discord.Intents.all()

cluster = MongoClient(CONNECTION_URL)
database = cluster["Manga-Update"]
collection = database["User-Data"]

# Setting up the bot
bot = commands.Bot(command_prefix='?',intents=intents,pass_context=True)

# Bot command add to list
@bot.command(name='list_add')
async def list_add(ctx):
    
    query = { "_id": str(ctx.message.author)}
    
    if collection.count_documents(query) == 0:
    
        reading_list = str(ctx.message.content).strip('?list_add ')
        reading_list = reading_list.split('/')
        
        url_list = getUrls(reading_list)
                
        post = {"_id": str(ctx.message.author), "Reading_List": reading_list, "Url_List": url_list}
                
        collection.insert_one(post)
        await ctx.channel.send("The Specified Manga have been added to your reading list!")
    
    else:
        user_data = collection.find(query)
        
        for data in user_data:
            reading_list = data["Reading_List"]
            url_list = data["Url_List"]      
           
        extend_reading = str(ctx.message.content).strip('?list_add ')
        extend_reading = extend_reading.split('/')
        
        extend_url = getUrls(extend_reading)
        
        reading_list.extend(extend_reading)
        url_list.extend(extend_url)
        
        collection.update_many({"_id": str(ctx.message.author)}, {"$set": {"Reading_List": reading_list,"Url_List": url_list}})
        await ctx.channel.send('The Specified Manga have been added to your reading list!')




bot.run(DISCORD_TOKEN)