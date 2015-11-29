#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    connection = psycopg2.connect("dbname=tournament user=vagrant")
    cursor = connection.cursor()
    return (connection, cursor)


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cur = connect()
    cur.execute("TRUNCATE TABLE matches;")
    conn.commit()
    conn.close()
    # print '*DELETED ALL matches*'
    return


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("TRUNCATE TABLE players;")
    conn.commit()
    conn.close()
    # print '*DELETED ALL players*'
    return


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    cur.execute("select count(*) as number from players;")
    (res, ) = cur.fetchone()
    conn.close()
    if res is None or res == '0':
        res = 0

    # print 'count players', res
    return res


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    cur.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()
    # print '*Register player*', name
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    sql = '''
    select s3.name, s1.id, s1.losses , s2.wins , s1.losses + s2.wins as matches from

    (select p.id, count(m.loser) as losses from players as p
    left join matches as m on (p.id = m.loser) group by p.id order by p.id)
    as s1

    left join

    (select p2.id, count(m2.winner) as wins from players as p2
    left join matches as m2 on (p2.id = m2.winner) group by p2.id
    order by p2.id)

    as s2 on (s1.id = s2.id)

    join (select id, name from players)
    as s3 on (s1.id = s3.id)

    order by s2.wins desc;
    '''
    cur.execute(sql)
    results = cur.fetchall()
    conn.close()

    standing = [(
        int(row[1]),  # id
        str(row[0]),  # name
        int(row[3]),  # wins
        int(row[4])   # matches
    ) for row in results]
    # print '*Standing*', standing
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cur = connect()
    cur.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);",(winner, loser))
    conn.commit()
    conn.close()
    # print 'Report new match', winner, loser


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    next_round = []
    standings = playerStandings()

    while len(standings) > 0:
        (id1, name1, win1, matches1) = standings.pop(0)
        (id2, name2, win2, matches2) = standings.pop(0)
        game = (id1, name1, id2, name2)
        next_round.append(game)

    # print next_round
    return next_round
