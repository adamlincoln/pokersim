from pokersim.Table import Table
from pokersim.Player import Player

def test_neverplay():
    table = Table()
    # Dealer will bet first preflop, so 2 will win as for now all players will fold
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10, 'NeverPlay')
        player.sit(table, i)
        players.append(player)
    assert table.button_seat == -1
    table.deal()
    assert table.button_seat == 0
    assert table.players[2].chips == 11
    assert table.players[1].chips == 9
    assert table.players[0].chips == 10
