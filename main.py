import os
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN  = os.getenv('DISCORD_TOKEN')
CONNECTION_URL = os.getenv('CONNECTION_URL')

intents = discord.Intents.all()

cluster = MongoClient(CONNECTION_URL)
database = cluster["User-Data"]
collection = database["User-Data"]
print("Database connected")

# Setting up the bot
bot = commands.Bot(command_prefix='?',intents=intents,pass_context=True)

# Bot command add to list
@bot.command(name='list_add')
async def list_add(ctx):
    
    reading_list = ctx.message.content.strip('?list_add ')
    reading_list = reading_list.split('/')
    print(reading_list)
    
    post = {"_id": ctx.message.author, "Reading_List": reading_list}
    
    
    print(str(ctx.message.author))
    print(str(ctx.message.channel))
    print(str(ctx.message.content))

bot.run(DISCORD_TOKEN)