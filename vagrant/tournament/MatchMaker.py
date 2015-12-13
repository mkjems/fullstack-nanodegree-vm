class MatchMaker:

    """A match maker class

    The main feature of this class is that it is able to
    pick pairs of players from a list of contenders.
    while making sure we do not 'paint ourselves into a corner'
    And by that I mean ending up with a player that has no
    oponents due the 'no-rematches' requirement

    It does so by relying on a list of posible contenders that it
    will be given by the function get_posible_games and the database view
    posible_games

    This class keeps making matches from the contender list using players that
    have the least number of possible oponents.
    """

    players = {}

    def __init__(self):
        self.players = {}

    def add_player(self, id, possible_oponents):
        self.players[id] = set(possible_oponents)

    def is_more(self):
        ''' This function tells if we have paired all contenders'''
        return bool(len(self.players))

    def make_match(self):
        ''' This function will return the best pair of players
        among the contenders'''

        # Find the player with the least options for an oponent
        # I call him 'shortest'

        # Make list of tuples of ids and number of possible oponents
        num_options = [
            (key, len(value)) for key, value in self.players.iteritems()
        ]
        # sort the list
        sorted_lengths = sorted(num_options, key=lambda player: player[1])
        # And take the one with least options.
        shortest = sorted_lengths.pop(0)[0]

        # In this players list of possible oponents, find the one with the
        # least options for an oponent
        # I call him 'oponent'
        oponents = self.players[shortest]
        oponents_options_nums = [(k, len(self.players[k])) for k in oponents]
        oponent = oponents_options_nums.pop(0)[0]

        game = set((shortest, oponent))

        # Remove shortest and oponent from players
        self.players.pop(shortest, None)
        self.players.pop(oponent, None)

        # Remove shortest and oponent from all sets.
        new_players = {
            key: (value - game) for key, value in self.players.iteritems()
        }
        self.players = new_players

        return (shortest, oponent)
