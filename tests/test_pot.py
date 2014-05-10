from pokersim.Table import Table
from pokersim.Pot import Pot

def test_pot_one():
    table = Table(1)
    pot = Pot(table.players)
    assert pot.chips == 0
    
def test_pot_init_1():
    table = Table(1)
    pot = Pot(table.players)
    assert pot.positions_eligible_to_win() == [0]

def test_pot_init_2():
    table = Table()
    pot = Pot(table.players)
    assert pot.positions_eligible_to_win() == [i for i in xrange(10)]

def test_pot_no_new_round_1():
    table = Table(1)
    pot = Pot(table.players)
    try:
        pot.receive_bet(0, 1)
    except AttributeError as e:
        pass
    else:
        assert False
    
def test_pot_receive_bet_1():
    table = Table(1)
    pot = Pot(table.players)
    assert not hasattr(pot, 'round_bets')
    pot.new_round()
    assert hasattr(pot, 'round_bets')
    assert pot.round_bets == {0: None}
    pot.receive_bet(0, 1)
    assert pot.round_bets == {0: 1}
    assert pot.chips == 0

def test_pot_receive_bet_2():
    table = Table(1)
    pot = Pot(table.players)
    pot.new_round()
    pot.receive_bet(0, 1)
    assert pot.chips == 0
    pot.end_round()
    assert pot.chips == 1

def test_pot_skim_1():
    table = Table(3)
    pot = Pot(table.players)
    pot.new_round()
    pot.receive_bet(0, 10)
    pot.receive_bet(1, 10)
    assert pot.round_bets == {0: 10, 1: 10, 2: None}
    assert pot.chips == 0
    for_next_pot = pot.skim_for_side_pot(7)
    assert pot.round_bets == {0: 7, 1: 7, 2: None}
    assert for_next_pot == {0: 3, 1: 3}

def test_pot_skim_2():
    table = Table(3)
    pot = Pot(table.players)
    pot.new_round()
    pot.receive_bet(0, 5)
    pot.receive_bet(1, 10)
    assert pot.round_bets == {0: 5, 1: 10, 2: None}
    assert pot.chips == 0
    for_next_pot = pot.skim_for_side_pot(7)
    assert pot.round_bets == {0: 5, 1: 7, 2: None}
    assert for_next_pot == {1: 3}

def test_pot_round_done_1():
    table = Table(3)
    pot = Pot(table.players)
    pot.new_round()
    assert not pot.round_done()
    pot.receive_bet(0, 5)
    assert not pot.round_done()
    pot.receive_bet(1, 10)
    assert not pot.round_done()
    pot.receive_bet(2, 10)
    assert not pot.round_done()
    pot.make_ineligible_to_win(0) # Player 0 folds
    assert pot.round_done()
    assert pot.round_bets == {1: 10, 2: 10}
    assert pot.chips == 5
    pot.end_round()
    assert pot.chips == 25
    assert not hasattr(pot, 'round_bets')

def test_pot_round_done_2():
    table = Table(3)
    pot = Pot(table.players)
    pot.new_round()
    assert not pot.round_done()
    pot.receive_bet(0, 0) # Check
    assert not pot.round_done()
    pot.receive_bet(1, 0)
    assert not pot.round_done()
    pot.receive_bet(2, 0)
    assert pot.round_done()


