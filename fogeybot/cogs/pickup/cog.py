import random
from discord.ext.commands import command

from .pickup import Pickup

class PickupCommands(object):
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel

        self.state = {}

    def in_correct_channel(self, ctx):
        if not self.channel:
            return True

        return ctx.message.channel.name == self.channel

    def get_server_pickup(self, ctx):
        return self.state.get(ctx.message.server, Pickup.inactive())

    def set_server_pickup(self, ctx, pickup):
        self.state[ctx.message.server] = pickup

    @command(description="Join an already-started pickup game. Format: <mmr>", no_pm=True, pass_context=True)
    async def joinpickup(self, ctx, mmr: int=1700):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if not pickup.active:
            await self.bot.say("No current pickup game, please start one with `!startpickup` first")
            return

        pickup.add_player(ctx.message.author.name, mmr)
        await self.bot.edit_message(pickup.status_message, "__Status__: %d/10 slots filled" % (len(pickup.players)))

        if len(pickup.players) == 10:
            team1, team2 = pickup.teams

            self.set_server_pickup(ctx, Pickup.inactive())

            random.shuffle(team1)
            random.shuffle(team2)

            assignments  = "Pickup team assignments balanced by MMR: \n"
            assignments += "__Team 1__: " + ", ".join([player.name for player in team1]) + "\n"
            assignments += "__Team 2__: " + ", ".join([player.name for player in team2])

            await self.bot.say(assignments)

    @command(description="Start a new pickup game", no_pm=True, pass_context=True)
    async def startpickup(self, ctx):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if pickup.active:
            return

        pickup = Pickup()
        self.set_server_pickup(ctx, pickup)

        await self.bot.say("**Pickup game starting!**")

        join_msg = "__To join__: type `!joinpickup 1700`%s, replacing 1700 with your MMR"
        if self.channel:
            channel_help = "in `#" + self.channel + "` "
        else:
            channel_help = ""

        await self.bot.say(join_msg.replace("%s", channel_help))
        pickup.status_message = await self.bot.say("__Status__: 0/10 slots filled")

    @command(description="Stop an already-started pickup game", no_pm=True, pass_context=True)
    async def stoppickup(self, ctx):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if pickup.status_message is not None:
            await self.bot.edit_message(pickup.status_message, "__Status__: stopped")

        self.set_server_pickup(ctx, Pickup.inactive())

        await self.bot.say("Pickup game stopped")
