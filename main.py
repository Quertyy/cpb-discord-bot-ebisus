from discord.ext import commands, tasks
import os, json
from dotenv import load_dotenv
import datetime, random, requests, discord

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COLLECTION_SLUG="CMB"
SALES_CHANNEL_ID = os.getenv("SALES_CHANNEL_ID")

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

@tasks.loop(minutes=1)
async def getLastSales():
    global lastSalesNumber
    url = "https://api.ebisusbay.com/listings?state=1&page=1&pageSize=1&sortBy=listingId&direction=desc&collection=0xA68825768bDB7a2161422e3CcAF1973FF88f8E66"
    now      = datetime.datetime.now() - datetime.timedelta(seconds=120)
    date     = now.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        response = requests.request("GET", url).json()
    except:
        pass
    try:
        for sales in response['listings']:
            if sales['listingId'] != lastSalesNumber:
                salesData = {}
                try :
                    salesData['nftName'] = sales['nft']['name']
                    salesData['imageUrl'] = sales['nft']['image']
                    salesData['seller'] = sales['seller'][0:8]
                    salesData['purchaser'] = sales['purchaser'][0:8]
                    salesData['price'] = sales['price']

                    embed = discord.Embed(title=f"{salesData['nftName']} Sold !", description="New Holder ?", color=discord.Colour.random())
                    embed.set_author(name="CPB Market", url="https://cronospb.com/")
                    embed.add_field(name="Seller", value=f"{salesData['seller']}", inline=True)
                    embed.add_field(name="Buyer", value=f"{salesData['purchaser']}", inline=True)
                    embed.add_field(name="Price", value=f"{salesData['price']} CRO", inline=True)
                    embed.set_image(url=salesData['imageUrl'])
                    embed.set_footer(text=f"Powered by #PrimatesTogether")
                    await bot.get_channel(SALES_CHANNEL_ID).send(embed=embed)
                except:
                    pass
        lastSalesNumber = sales['listingId']
    except:
        pass

@getFloorPrice.before_loop
async def before():
    await bot.wait_until_ready()

@getLastSales.before_loop
async def before():
    await bot.wait_until_ready()
    
@bot.event
async def on_ready():
    print("Bot is ready !")
    getFloorPrice.start()
    getLastSales.start()
    
bot.run(DISCORD_TOKEN)