#!/usr/bin/env python

# Simulation of a 16 player swiss style tounament

import random
import math
import time
from tournament import *


def play16PLayerTournament():
    # reset
    deleteMatches()
    deletePlayers()

    newPlayers = [
        "Twilight Sparkle",
        "Fluttershy",
        "Applejack",
        "Mister X",
        "Pinkie Pie",
        "Cotten Eye Joe",
        "President Obama",
        "Whinston Churchill",
        "Lou Reed",
        "Benjamin Franklin",
        "Michal Jackson",
        "Sylvester Stalone",
        "Madonna",
        "Richard Nixon",
        "Steve Jobs",
        "Bill Gates"
    ]

    print "Number of new players:", len(newPlayers)
    # register players
    for player in newPlayers:
        registerPlayer(player)

    # Calculate number of rounds
    number_of_rounds = int(math.log(len(newPlayers), 2))

    print "This tounament will take {} rounds".format(number_of_rounds)

    for round in range(1, number_of_rounds+1):

        print "\nWe're in round %d" % (round)

        # Pair
        pairings = swissPairings()

        # Register
        for pair in pairings:
            p = [pair[0], pair[2]]
            # Find a random winner
            random.shuffle(p)
            reportMatch(p[0], p[1])
        time.sleep(0)

        # Standings
        print '\nStandings after round', round, '\n'
        standings = playerStandings()
        for plr in standings:
            print plr

        # Test that all the oponent histories do not contain duplicates
        standings = playerStandings()
        for player in standings:
            history = oponentHistory(player[0])
            if(len(history) != len(set(history))):
                raise ValueError(
                    "Each player should only play an oponent once.")
            if(len(history) != round):
                raise ValueError(
                    "After round {} each player should have"
                    " played {} oponents".format(round, round))

        # raw_input('OK')

if __name__ == '__main__':
    play16PLayerTournament()
    print "Success! tournament complete"
