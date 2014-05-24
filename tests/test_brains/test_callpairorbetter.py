from pokersim.Table import Table
from pokersim.Player import Player
from pokersim.Card import Card
from pokersim.Decision import Decision

def test_callpairorbetter_fold_preflop():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'CallPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('H', 10))
    table.players[0].hole_cards.append(Card('H', 9))
    assert table.players[0].decide() == Decision.FOLD

def test_callpairorbetter_call_preflop():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'CallPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 9))
    table.players[0].hole_cards.append(Card('H', 9))
    assert table.players[0].decide() == Decision.CALL

def test_callpairorbetter_call_postflop():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'CallPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 9))
    table.players[0].hole_cards.append(Card('H', 9))
    table.board.append(Card('S', 'A'))
    assert table.players[0].decide() == Decision.CALL

