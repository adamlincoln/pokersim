from pokersim.Table import Table
from pokersim.Player import Player
from pokersim.Card import Card
from pokersim.Decision import Decision

def test_foldwithnopostfloppairorbetter_call_preflop():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'FoldWithNoPostFlopPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 2))
    table.players[0].hole_cards.append(Card('H', 9))
    assert table.players[0].decide() == Decision.CALL

def test_foldwithnopostfloppairorbetter_call_postflop_1():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'FoldWithNoPostFlopPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 9))
    table.players[0].hole_cards.append(Card('H', 9))
    table.board.append(Card('S', 10))
    table.board.append(Card('S', 10))
    table.board.append(Card('S', 10))
    assert table.players[0].decide() == Decision.CALL

def test_foldwithnopostfloppairorbetter_call_postflop_2():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'FoldWithNoPostFlopPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 9))
    table.players[0].hole_cards.append(Card('H', 9))
    table.board.append(Card('S', 'K'))
    table.board.append(Card('S', 3))
    table.board.append(Card('S', 7))
    assert table.players[0].decide() == Decision.CALL

def test_foldwithnopostfloppairorbetter_fold_postflop():
    table = Table()
    num_players = 3
    for i in xrange(num_players):
        player = Player(10, 'FoldWithNoPostFlopPairOrBetter')
        player.sit(table, i)
    table.initialize_hand()
    table.players[0].hole_cards.append(Card('D', 2))
    table.players[0].hole_cards.append(Card('H', 9))
    table.board.append(Card('S', 'K'))
    table.board.append(Card('S', 3))
    table.board.append(Card('S', 7))
    assert table.players[0].decide() == Decision.FOLD

