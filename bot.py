import asyncio
import os
import random
import re
import time

import discord

email = os.environ["DISCORD_EMAIL"]
password = os.environ["DISCORD_PASSWORD"]

client = discord.Client()

start_time = 0
players = []

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global start_time
    global players

    if message.channel.name != "pickup":
        return

    if message.content.startswith("!startpickup"):
        if active_game(start_time):
            return

        start_time = time.time()
        players = []

        await client.send_message(message.channel, "Pickup game starting!")
        await client.send_message(message.channel, "To join, type !joinpickup MMR, filling in your MMR (e.g. !joinpickup 2200)")

        print("Starting pickup...")

    elif message.content.startswith("!stoppickup"):
        start_time = 0
        players = []

        await client.send_message(message.channel, "Pickup game abandoned")

        print("Stopping pickup")

    elif message.content.startswith("!joinpickup"):
        if not active_game(start_time):
            await client.send_message(message.channel, "No current pickup game, please start one with !startpickup first")
            return

        mmr = parse_mmr(message.content)
        if mmr is None:
            return

        if mmr < 400 or mmr > 5000:
            mmr = 1500

        players.append(Player(message.author.name, mmr))

        print("Added %s to player pool" % (message.author.name))

        if len(players) == 10:
            team1, team2 = assign_teams(players)

            start_time = 0
            players = []

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

def active_game(start_time, now=None):
    if now is None:
        now = time.time()

    return (now - start_time) < 5 * 60

class Player(object):
    def __init__(self, name, mmr):
        self.name = name
        self.mmr = mmr

def assign_teams(players):
    team1 = []
    team2 = []

    players_by_mmr = sorted(players, key=lambda p: p.mmr)

    while players_by_mmr:
        p1 = players_by_mmr.pop()
        p2 = players_by_mmr.pop()

        if len(team1) % 2 == 0:
            team1.append(p1)
            team2.append(p2)
        else:
            team1.append(p2)
            team2.append(p1)

    return team1, team2

client.run(email, password)
