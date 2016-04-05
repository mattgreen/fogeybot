import random
import re

from discord.ext.commands import command

from fogeybot.errors import APIError

from .pickup import Pickup

class PickupCommands(object):
    DEFAULT_MMR = 1500

    def __init__(self, bot, api, db, channel):
        self.bot = bot
        self.api = api
        self.db = db
        self.channel = channel

        self.maps = None
        self.state = {}

    def in_correct_channel(self, ctx):
        if not self.channel:
            return True

        channel = ctx.message.channel.name

        return re.sub("[^a-zA-Z0-9]", "", channel).lower() == self.channel.lower()

    def get_server_pickup(self, ctx):
        return self.state.get(ctx.message.server, Pickup.inactive())

    def set_server_pickup(self, ctx, pickup):
        self.state[ctx.message.server] = pickup

    async def on_pickup_updated(self, ctx, pickup):
        await self.bot.edit_message(pickup.status_message, "__Status__: %d/10 slots filled" % (len(pickup.players)))

        if len(pickup.players) == 10:
            team1, team2 = pickup.teams

            self.set_server_pickup(ctx, Pickup.inactive())

            random.shuffle(team1.members)
            random.shuffle(team2.members)

            assignments = "Pickup team assignments: \n"
            assignments += "__Team 1__: {} (avg MMR: {})\n".format(", ".join(team1.members), team1.mean_mmr)
            assignments += "__Team 2__: {} (avg MMR: {})\n".format(", ".join(team2.members), team2.mean_mmr)

            await self.bot.say(assignments)

    @command(description="Manually add a player to a pickup. Format: <name> <mmr>", no_pm=True, pass_context=True)
    async def addpickup(self, ctx, name: str, mmr: int=DEFAULT_MMR):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if not pickup.active:
            await self.bot.say("No current pickup game, please start one with `!startpickup` first")
            return

        pickup.add_player(name, mmr)

        await self.on_pickup_updated(ctx, pickup)

    @command(description="Join an already-started pickup game. Format: <mmr>", no_pm=True, pass_context=True)
    async def joinpickup(self, ctx, mmr: int=0):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if not pickup.active:
            await self.bot.say("No current pickup game, please start one with `!startpickup` first")
            return

        if mmr == 0:
            mmr = None

        # No MMR specified? Try to look it up for them
        discord_id = ctx.message.author.id

        if mmr is None:
            try:
                battle_tag = await self.db.lookup_battle_tag(discord_id)
                if battle_tag is not None:
                    mmr_info = await self.api.get_mmr(battle_tag)
                    if mmr_info.present:
                        mmr = mmr_info.mmr
                        await self.db.set_mmr(discord_id, mmr)

                        print("Fetched MMR for {}: {}".format(battle_tag, mmr))

            except APIError:
                mmr = await self.db.get_mmr(discord_id)
                if mmr is None:
                    self.bot.say("Sorry, I'm having trouble talking to HotsLogs right now")

        # If we still don't have an MMR, use the default
        if mmr is None:
            mmr = self.DEFAULT_MMR

        pickup.add_player(ctx.message.author.name, mmr)

        await self.on_pickup_updated(ctx, pickup)

    @command(description="Abandon your slot in the current pickup", no_pm=True, pass_context=True)
    async def leavepickup(self, ctx):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if not pickup.active:
            return

        pickup.remove_player(ctx.message.author.name)

        await self.on_pickup_updated(ctx, pickup)

    @command(description="Show who has joined the pickup", no_pm=True, pass_context=True)
    async def pickupstatus(self, ctx):
        if not self.in_correct_channel(ctx):
            return

        pickup = self.get_server_pickup(ctx)
        if not pickup.active:
            await self.bot.say("No current pickup game, please start one with `!startpickup` first")
            return

        players = sorted(pickup.players, key=lambda p: p.name)

        status = "Pickup Status: \n"
        status += "__Info__: {}/10 slots filled\n".format(len(players))
        status += "__Players__: {}\n".format(", ".join(["{} ({})".format(p.name, p.mmr) for p in players]))

        await self.bot.say(status)

    @command(description="Choose a random map", pass_context=True)
    async def randommap(self, ctx):
        def allowed_map(m):
            exclusions = ["mines", "cavern"]

            for exclusion in exclusions:
                if exclusion in m.lower():
                    return False

            return True

        if not self.in_correct_channel(ctx):
            return

        if self.maps is None:
            try:
                self.maps = [m for m in await self.api.get_maps() if allowed_map(m)]

            except APIError:
                pass

        if self.maps is not None:
            selected_map = random.choice(self.maps)
            await self.bot.say("Random map: " + selected_map)
        else:
            await self.bot.say("Sorry, I can't get the map list right now! Try again later.")

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
