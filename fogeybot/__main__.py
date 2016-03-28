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

config = {}
if "VCAP_SERVICES" in os.environ:
    config = json.loads(os.environ["VCAP_SERVICES"])["rediscloud"][0]["credentials"]
else:
    config = { "hostname": "localhost", "port": 6379, "password": None }

email = os.environ["DISCORD_EMAIL"]
password = os.environ["DISCORD_PASSWORD"]
channel = os.environ.get("DISCORD_CHANNEL")

db = Database(config["hostname"], config["port"], config["password"])
asyncio.get_event_loop().run_until_complete(db.connect())

api = HotsLogsAPI()

bot.add_cog(GeneralCommands(bot))
bot.add_cog(PickupCommands(bot, api, channel))
bot.add_cog(UserCommands(bot, api, db))
bot.run(email, password)
