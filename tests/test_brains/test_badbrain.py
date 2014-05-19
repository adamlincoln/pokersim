from pokersim.Table import Table
from pokersim.Player import Player
from pokersim.Player import PlayerException

def test_badbrain():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        try:
            player = Player(10, 'NotARealBrainName')
        except PlayerException as e:
            assert str(e) == 'Brain named "NotARealBrainName" cannot be found'

