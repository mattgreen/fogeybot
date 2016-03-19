import os

from discord.ext.commands import Bot

from fogeybot.hotslogs_api import HotsLogsAPI
from fogeybot.cogs.general.cog import GeneralCommands
from fogeybot.cogs.pickup.cog import PickupCommands

bot = Bot(command_prefix="!", description="I am FogeyBot! I help start pickup games, and do other bot-y things.")

@bot.event
async def on_ready():
    print("FogeyBot: logged in as %s" % (bot.user.name))

email = os.environ["DISCORD_EMAIL"]
password = os.environ["DISCORD_PASSWORD"]
channel = os.environ.get("DISCORD_CHANNEL")

api = HotsLogsAPI()

bot.add_cog(GeneralCommands(bot))
bot.add_cog(PickupCommands(bot, api, channel))

bot.run(email, password)
