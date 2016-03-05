## Introduction

A simple Discord bot written with discord.py for forming teams for pickup games. Right now, it's made with Heroes of the Storm in mind.

Someone starts a pickup game, then players join the pickup in progress. After ten players have joined, the MMRs specified are used to produce two teams of approximately equal skill.

The balancing algorithm works by sorting players by their skill, pairing players with the closest player of approximate skill, and splitting the pair between teams. To prevent team 1 from being weighted too heavily towards better players, we alternate which team the first player of a pair is assigned to.

Currently, this is **alpha quality**! It hasn't been used for any pickup games...yet.

## Commands

### !startpickup

Starts a new pickup game

### !joinpickup [mmr]

Adds the player to the current pickup game with the given MMR. If it is not specified, use a default MMR of 1700.

If the MMR is not parsable, or is outside a reasonable range of MMRs, it is ignored.

### !stoppickup

Stops the pickup game.

Games should expire after 5 minutes of the first `!startpickup` command.

## Deploying

Files for running on Heroku are included.
