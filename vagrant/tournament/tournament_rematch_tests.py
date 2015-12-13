#!/usr/bin/env python
#
# Test cases for rematches

from tournament import *


def testRematchAttemptisIgnored():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id1, id2)

    id1_hist = oponentHistory(id2)
    if(len(id1_hist) > 1):
        raise ValueError(
            "Rematches are not allowed and should be ignored"
        )

    else:
        print 'OK - rematch ignored'


def testReverseRematchAttemptIsIgnored():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id2, id1)

    id1_hist = oponentHistory(id2)
    if(len(id1_hist) > 1):
        raise ValueError(
            "Reverse rematches are not allowed and should be ignored"
        )

    else:
        print 'OK - reverse rematch ignored'

if __name__ == '__main__':
    testRematchAttemptisIgnored()
    testReverseRematchAttemptIsIgnored()
    print "Success! tests pass!"
