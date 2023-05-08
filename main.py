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

# Bot command show list
@bot.command(name='list')
async def list(ctx):
    query = { "_id": str(ctx.message.author)}
    
    if collection.count_documents(query) == 0:
        await ctx.channel.send("You do not have a reading list made! Please make one using the ?list_add command!")
    
    for data in collection.find(query):
        reading_list = data["Reading_List"]
        
    if len(reading_list) == 0:
        await ctx.channel.send("Your reading list is empty! Please make one using the ?list_add command!") 

    else:
        counter = 1
        
        message = f'Hey {ctx.message.author.mention} Your reading list is comprised of: \n'
        
        for manga in reading_list:
            message += str(counter) + ") " + manga + "\n"
            counter += 1
        
        await ctx.channel.send(message)
    
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
        await ctx.channel.send("The specified Manga have been added to your reading list!")
    
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
        await ctx.channel.send('The specified Manga have been added to your reading list!')

# Bot command remove from list
@bot.command(name='list_remove')
async def list_remove(ctx):
    
    query = { "_id": str(ctx.message.author)}
    
    if collection.count_documents(query) == 0:
        await ctx.channel.send("You do not have a reading list made! Please make one using the ?list_add command!")
    
    for data in collection.find(query):
        reading_list = data["Reading_List"]
        url_list = data["Url_List"]
        
    if len(reading_list) == 0:
        await ctx.channel.send("Your reading list is empty! Please make one using the ?list_add command!") 
    else:
        tb_removed_list = str(ctx.message.content).strip('?list_remove ')
        tb_removed_list = tb_removed_list.split('/')
        
        for index in range(len(tb_removed_list)):
            if tb_removed_list[index] in reading_list:
                reading_list.remove(tb_removed_list[index])
                url_list.pop(index)
        
        collection.update_many({"_id": str(ctx.message.author)}, {"$set": {"Reading_List": reading_list,"Url_List": url_list}})
        await ctx.channel.send('The specified Manga have been removed from your reading list!')

# Bot command delete list
@bot.command(name='delete_list')
async def delete_list(ctx):
    query = { "_id": str(ctx.message.author)}
    
    if collection.count_documents(query) == 0:
        await ctx.channel.send("You do not have a reading list made! Please make one using the ?list_add command!")
    else:
        collection.delete_one(query)
        await ctx.channel.send("Reading list deleted successfully!")
    
bot.run(DISCORD_TOKEN)