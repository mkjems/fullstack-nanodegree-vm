#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import pprint

pp = pprint.PrettyPrinter(indent=4)


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
        select * from standings;
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


def oponentHistory(id):
    """ Returns the list of oponents ids a player as already played in this
    tournament
    Arg: player id
    """
    conn, cur = connect()
    sql = '''
        (select loser as oponents from matches where  winner={} )
        union all
        (select winner as oponents from matches where  loser={} )
    '''
    sql = sql.format(id, id)
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    result = [row[0] for row in rows]

    # print '********************************'
    # print '*id*', id
    # print '*Oponent history*', result
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cur = connect()
    sql = '''
        INSERT INTO matches (winner, loser)
        VALUES (%s, %s);
    '''
    cur.execute(sql, (winner, loser))
    conn.commit()
    conn.close()
    # print 'Report new match', winner, loser


def get_tounament_player_dict():
    ''' Read the payer names and id'''
    conn, cur = connect()
    sql = '''
        select * from players;
    '''
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    result = {int(row[0]): str(row[1]) for row in rows}
    return result


def get_posible_games():
    ''' Returns a datastucture where all the players are grouped by number of wins
    and have a list of all their possible oponents for the next game.
    '''
    conn, cur = connect()
    sql = '''
        select * from posible_games;
    '''
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    result = {}
    for row in rows:
        (id, oponent_id, wins) = row
        result.setdefault(
            int(wins), {}).setdefault(int(id), []).append(int(oponent_id))
    return result


class MatchMaker:
    """A match maker class"""

    players = {}

    def __init__(self):
        self.players = {}

    def add_player(self, id, possible_oponents):
        self.players[id] = set(possible_oponents)

    def is_more(self):
        return bool(len(self.players))

    def make_match(self):
        # find the player with the least options for an oponent
        num_options = [(key, len(value)) for key, value in self.players.iteritems()]
        sorted_lengths = sorted(num_options, key=lambda player: player[1])
        shortest = sorted_lengths.pop(0)[0]

        # In this players list of possible oponents, find the one with the
        # least options for an oponent '''
        oponents = self.players[shortest]
        oponents_options_nums = [(k, len(self.players[k])) for k in oponents]
        oponent = oponents_options_nums.pop(0)[0]

        game = set((shortest, oponent))

        # Remove shortest and oponent from players
        self.players.pop(shortest, None)
        self.players.pop(oponent, None)

        # Remove shortest and oponent from all sets.
        new_players = {key: (value - game) for key, value in self.players.iteritems()}
        self.players = new_players

        return (shortest, oponent)


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
    posible_games = get_posible_games()
    player_dict = get_tounament_player_dict()

    # Iterate through the groups of players with same num wins
    for group in posible_games:
        # Create a matchmaker and feed it all the players for this group
        match_maker = MatchMaker()
        for player in posible_games[group]:
            match_maker.add_player(player, posible_games[group][player])

        # Keep making matches until there are no more players
        while match_maker.is_more():
            (player1_id, player2_id) = match_maker.make_match()
            next_round.append((
                player1_id,
                player_dict[player1_id],
                player2_id,
                player_dict[player1_id]
            ))

    return next_round
