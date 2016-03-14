import asyncio
import os
import random
import re
import time

import discord

from fogeybot.pickup import Pickup

client = discord.Client()

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

    # TODO: don't hardcode this
    if message.channel.name != "pickup":
        return

    if message.content.startswith("!startpickup"):
        if pickup.active:
            return

        pickup = Pickup()

        await client.send_message(message.channel, "Pickup game starting!")
        await client.send_message(message.channel, "To join, type !joinpickup MMR, filling in your MMR (e.g. !joinpickup 2200)")

        print("Starting pickup...")

    elif message.content.startswith("!stoppickup"):
        pickup = Pickup.inactive()

        await client.send_message(message.channel, "Pickup game abandoned")

        print("Stopping pickup")

    elif message.content.startswith("!joinpickup"):
        if not pickup.active:
            await client.send_message(message.channel, "No current pickup game, please start one with !startpickup first")
            return

        mmr = parse_mmr(message.content)
        if mmr is None:
            return

        pickup.add_player(message.author.name, mmr)

        print("Added/updated %s in player pool" % (message.author.name))

        if len(pickup.players) == 10:
            team1, team2 = pickup.teams

            pickup = Pickup.inactive()

            random.shuffle(team1)
            random.shuffle(team2)

            assignments  = "Pickup team assignments balanced by MMR: \n"
            assignments += "Team 1: " + ", ".join([player.name for player in team1]) + "\n"
            assignments += "Team 2: " + ", ".join([player.name for player in team2])

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

email = os.environ["DISCORD_EMAIL"]
password = os.environ["DISCORD_PASSWORD"]
client.run(email, password)
