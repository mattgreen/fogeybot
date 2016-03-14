## Introduction

A simple Discord bot written with discord.py for forming teams for pickup games.

Right now, it's made with Heroes of the Storm in mind, though it should work for any game.

## Running

FogeyBot pulls login information from environment variables:

    $ DISCORD_EMAIL="bot_email@example.com" DISCORD_PASSWORD="bot_password" python -m fogeybot

You can configure the bot to only listen for commands on a certain channel by setting the `DISCORD_CHANNEL` env var, as well.

## Usage

Someone starts a pickup game via the `!startpickup` command, then players join the pickup in progress using `!joinpickup`. After ten players have joined, the MMRs specified are used to produce two teams of approximately equal skill. You can abort the game early using the `!stoppickup` command.

The balancing algorithm works by sorting players by their skill, pairing players with the closest player of approximate skill, and splitting the pair between teams. To prevent team 1 from being weighted too heavily towards better players, we alternate which team the first player of a pair is assigned to.

## Status

Currently, this is **alpha quality**! It hasn't been used for any pickup games...yet.

## Commands

### !startpickup

Starts a new pickup game

### !joinpickup [mmr]

Adds the player to the current pickup game with the given MMR. If it is not specified, use a default MMR of 1700.

If the MMR is not parsable, it is ignored. If it is outside a reasonable range, it defaults to 1700.

### !stoppickup

Stops the pickup game.

Games expire after 5 minutes of the first `!startpickup` command.

## Deploying

Files for running on BlueMix are included.
