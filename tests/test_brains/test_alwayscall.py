from pokersim.Table import Table
from pokersim.Player import Player

def test_alwayscall():
    table = Table()
    # Dealer will bet first preflop, so 2 will win as for now all players will fold
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10, 'AlwaysCall')
        player.sit(table, i)
        players.append(player)
    assert table.button_seat == -1
    table.deal()
    assert table.button_seat == 0
    # I don't know who won here
    chips = []
    for player in table.players.values():
        chips.append(player.chips)
    assert (chips.count(8) == 2 and chips.count(14) == 1) or \
           (chips.count(8) == 2 and chips.count(14) == 1) or \
           (chips.count(10) == 3)
