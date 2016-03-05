# Introduction

A simple Discord bot for forming teams for pickup games. Right now, it's made with Heroes of the Storm in mind.

# Status

Alpha-quality! Hasn't been used for any pickup games...yet.

# Commands

### !startpickup

Starts a new pickup game

### !joinpickup [mmr]

Adds the player to the current pickup game with the given MMR. If it is not specified, use a default MMR of 1700.

If the MMR is not parsable, or is outside a reasonable range of MMRs, it is ignored.

### !stoppickup

Stops the pickup game.

Games should expire after 5 minutes of the first `!startpickup` command.

# Deploying

Files for running on Heroku are included.
