import asyncio
import json
import os

from discord.ext.commands import Bot

from fogeybot.database import Database
from fogeybot.hotslogs_api import HotsLogsAPI

from fogeybot.cogs.general.cog import GeneralCommands
from fogeybot.cogs.pickup.cog import PickupCommands
from fogeybot.cogs.users import UserCommands

bot = Bot(command_prefix="!", description="I am FogeyBot! I help start pickup games, and do other bot-y things.")

@bot.event
async def on_ready():
    print("FogeyBot: logged in as %s" % (bot.user.name))

client_id = os.environ["DISCORD_CLIENT_ID"]
token = os.environ["DISCORD_TOKEN"]
channel = os.environ.get("DISCORD_CHANNEL")
uri = os.environ["MONGO_URI"]

db = Database(uri)
asyncio.get_event_loop().run_until_complete(db.test_connection())

api = HotsLogsAPI()

bot.add_cog(GeneralCommands(bot))
bot.add_cog(PickupCommands(bot, api, db, channel))
bot.add_cog(UserCommands(bot, api, db))

bot.client_id = client_id
bot.run(token)
