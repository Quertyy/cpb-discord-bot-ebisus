from discord.ext import commands, tasks
import os, json
from dotenv import load_dotenv
import datetime, random, requests, discord

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COLLECTION_SLUG="CMB"

intents           = discord.Intents.default()
intents.members   = True
bot               = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

@tasks.loop(minutes=1)
async def getFloorPrice():
    url        = "https://api.ebisusbay.com/collections?collection=0x939b90c529F0e3a2C187E1b190Ca966a95881FDe"
    url2       = "https://api.ebisusbay.com/collections?collection=0xc843f18d5605654391e7eDBEa250f6838C3e8936"
    try:
        response = requests.request("GET", url).json()
        response2 = requests.request("GET", url2).json()
        floorPriceCMB = response["collections"][0]['floorPrice']
        floorPriceCGB = response2["collections"][0]['floorPrice']
        await bot.change_presence(activity=discord.Game(name=f'FP CMB: {floorPriceCMB} CRO | FP CGB: {floorPriceCGB} CRO'))
    except:
        pass

#@tasks.loop(minutes=1)
#@bot.command(name='volume')
#async def getVolume():
#    url       = "https://api.ebisusbay.com/collections?collection=0x939b90c529F0e3a2C187E1b190Ca966a95881FDe"
#    try:
#        response = requests.request("GET", url).json()
#        volume = response["collections"][0]['totalVolume']
#    except:
#        pass
    
@getFloorPrice.before_loop
async def before():
    await bot.wait_until_ready()
    
@bot.event
async def on_ready():
    print("Bot is ready !")
    getFloorPrice.start()
    
bot.run(DISCORD_TOKEN)