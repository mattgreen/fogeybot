import asyncio
import os
import random
import re

import discord

from fogeybot.pickup import Pickup

client = discord.Client()

email = os.environ["DISCORD_EMAIL"]
password = os.environ["DISCORD_PASSWORD"]
channel = os.environ.get("DISCORD_CHANNEL")

# Global state
pickup = Pickup.inactive()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global pickup

    if channel:
        if message.channel.name != channel:
            return

    if message.content.startswith("!startpickup"):
        if pickup.active:
            return

        pickup = Pickup()

        await client.send_message(message.channel, "**Pickup game starting!**")

        join_msg = "__To join__: type `!joinpickup 1700`%s, replacing 1700 with your MMR"
        if channel:
            channel_help = "in `#" + channel + "` "
        else:
            channel_help = ""

        await client.send_message(message.channel, join_msg.replace("%s", channel_help))
        pickup.status_message = await client.send_message(message.channel, "__Status__: 0/10 slots filled")

        print("Starting pickup...")

    elif message.content.startswith("!stoppickup"):
        msg = pickup.status_message
        pickup = Pickup.inactive()

        if msg is not None:
            await client.edit_message(msg, "__Status__: stopped")

        await client.send_message(message.channel, "Pickup game stopped")

        print("Stopping pickup")

    elif message.content.startswith("!joinpickup"):
        if not pickup.active:
            await client.send_message(message.channel, "No current pickup game, please start one with `!startpickup` first")
            return

        mmr = parse_mmr(message.content)
        if mmr is None:
            return

        pickup.add_player(message.author.name, mmr)
        await client.edit_message(pickup.status_message, "__Status__: %d/10 slots filled" % (len(pickup.players)))

        print("Added/updated %s in player pool" % (message.author.name))

        if len(pickup.players) == 10:
            team1, team2 = pickup.teams

            pickup = Pickup.inactive()

            random.shuffle(team1)
            random.shuffle(team2)

            assignments  = "Pickup team assignments balanced by MMR: \n"
            assignments += "__Team 1__: " + ", ".join([player.name for player in team1]) + "\n"
            assignments += "__Team 2__: " + ", ".join([player.name for player in team2])

            await client.send_message(message.channel, assignments)

            print("Assigned teams")


def parse_mmr(s, default=1700):
    parts = re.split("\s+", s.strip())
    if len(parts) == 1:
        return default

    try:
        return int(parts[1])
    except ValueError:
        return None

client.run(email, password)
