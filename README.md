## Introduction [![Build Status](https://travis-ci.org/mattgreen/fogeybot.svg?branch=master)](https://travis-ci.org/mattgreen/fogeybot)

A simple Discord bot written with `discord.py` for forming teams for pickup games.

It's tailored towards Heroes of the Storm.

## Prerequisites

* Python 3.5
* A Discord bot user and client ID
* Somewhere to run it (VPS, Heroku, BlueMix, etc)
* MongoDB for persisted information

## Running

First, clone the repo:

    $ git clone https://github.com/mattgreen/fogeybot.git
    $ cd fogeybot

Next, install dependencies:

    $ pip install -r requirements.txt

Finally, start FogeyBot, specifying login information in environment variables:

    $ DISCORD_CLIENT_ID="client_id" DISCORD_TOKEN="bot_token" MONGO_URI="uri" python -m fogeybot

You can configure the bot to only listen for commands on a certain channel by setting the `DISCORD_CHANNEL` env var, as well.

## Usage

Someone starts a pickup game via the `!startpickup` command, players can join the pickup in progress using the `!joinpickup 1700` command, where `1700` is their MMR. After ten players have joined, the MMRs specified are used to produce two teams of approximately equal skill. 

You can abort the game early using the `!stoppickup` command.

The balancing algorithm works by sorting players by their skill, pairing players with the closest player of approximate skill, and splitting the pair between teams. To prevent team 1 from being weighted too heavily towards better players, we alternate which team the first player of a pair is assigned to.

## Status

This is used regularly to host pickup games for Fogey League.

## Commands

### General
#### !help

Prints help information

#### !uptime

Prints uptime information. Useful for monitoring how good your hosting is.

#### !coinflip

Flips a coin


### Pickup

#### !startpickup

Starts a new pickup game

#### !addpickup name [mmr]

Adds the specified player to the current pickup game with the given MMR. If it is not specified, use a default MMR of 1500. This command is useful for quickly on-boarding new users.

If the MMR is not parsable, it is ignored. If it is outside a reasonable range, it defaults to 1500.

#### !joinpickup [mmr]

Adds the player to the current pickup game with the given MMR. 

If the user has registered their battle tag (via `!register`), and no MMR is specified, it will be retrieved from HotsLogs.
If the user has not registered their battle tag, or their HL profile is private, then use a default MMR of 1500.

If the MMR is not parsable, it is ignored. If it is outside a reasonable range, it defaults to 1500.

#### !pickupstatus

Prints out information about the current pickup, including who has joined and their MMR

#### !leavepickup

Removes your pickup slot, freeing it up for someone else.

#### !stoppickup

Stops the pickup game.

Games expire after 30 minutes of the first `!startpickup` command.

#### !randommap

Prints a random map, excluding Haunted Mines and Lost Cavern.

### User registration

#### !register battletag#123

Associates the user's battle.net ID with the Discord account

#### !registrationstatus

Returns the user's battle.net ID, if any

#### !unregister

Removes the user's battle.net ID information, if any

## Deploying

Files for running on BlueMix are included.
