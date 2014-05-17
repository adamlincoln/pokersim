from pokersim.Player import Player
from pokersim.Table import Table
from pokersim.Decision import Decision

def test_player():
    player = Player(10)
    assert player.chips == 10
    assert repr(player) == '<Player Pos:   Hole Cards:   Chips: 10>'

def test_player_with_table():
    player = Player(10)
    table = Table()
    player.sit(table, 0)
    assert player.table == table
    assert player.position == 0
    assert repr(player) == '<Player Pos: 0  Hole Cards:   Chips: 10>'

def test_player_decision():
    player = Player(3)
    assert player.decide() == Decision.FOLD # Default for now

def test_player_decision_forced():
    player = Player(3)
    assert player.decide(force=Decision.FOLD) == Decision.FOLD # Default for now

def test_player_discard_hole_cards():
    player = Player(3)
    player.hole_cards.append('fake')
    player.discard_hole_cards()
    assert player.hole_cards == []
