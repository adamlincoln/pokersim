from pokersim.Player import Player
from pokersim.Pot import Pot
from pokersim.Pot import PotException

num_players = 10

def test_new_pot():
    pot = Pot(range(num_players))
    assert pot.chips == 0
    round_bets_keys = pot.round_bets.keys()
    round_bets_keys.sort()
    assert round_bets_keys == range(10)

def test_pot_ineligible_position_bet():
    pot = Pot(range(num_players))
    assert pot.round_bets == dict(zip(range(10), [None for pos in range(10)]))
    try:
        pot.receive_bet(1, 11)
    except PotException as e:
        assert str(e) == 'Position 11 is not eligible to win'
    else:
        assert False

def test_pot_receive_bet():
    pot = Pot(range(num_players))
    pot.receive_bet(10, 0)
    compare_round_bets = dict(zip(range(1, 10), [None for pos in range(1, 10)]))
    compare_round_bets[0] = 10
    assert pot.round_bets == compare_round_bets
    assert pot.chips == 0

def test_pot_single_player_end_round():
    pot = Pot(range(1))
    pot.receive_bet(10, 0)
    assert pot.round_bets == {0: 10}
    assert pot.chips == 0
    pot.end_round()
    assert pot.round_bets == {0: None}
    assert pot.chips == 10

def test_pot_three_players_end_round():
    pot = Pot(range(3))
    assert not pot.round_done()
    pot.receive_bet(5, 0)
    assert not pot.round_done()
    pot.receive_bet(10, 1)
    assert not pot.round_done()
    pot.receive_bet(10, 2)
    assert not pot.round_done()
    pot.make_ineligible_to_win(0) # Player 0 folds
    assert pot.round_done()
    assert pot.round_bets == {1: 10, 2: 10}
    assert pot.chips == 5
    pot.end_round()
    assert pot.chips == 25
    assert pot.round_bets == {1: None, 2: None}

def test_pot_three_players_bad_fold():
    pot = Pot(range(3))
    assert not pot.round_done()
    pot.receive_bet(5, 0)
    assert not pot.round_done()
    pot.make_ineligible_to_win(1)
    assert not pot.round_done()
    pot.receive_bet(10, 2)
    assert not pot.round_done()
    pot.receive_bet(5, 0) # Player 0 calls
    assert pot.round_done()
    assert pot.round_bets == {0: 10, 2: 10}
    assert pot.chips == 0
    try:
        pot.make_ineligible_to_win(1)
    except PotException as e:
        assert str(e) == 'Position 1 is already not eligible to win'
    else:
        assert False

def test_pot_three_players_end_round_2():
    pot = Pot(range(3))
    assert not pot.round_done()
    pot.receive_bet(0, 0) # Check
    assert not pot.round_done()
    pot.receive_bet(0, 1)
    assert not pot.round_done()
    pot.receive_bet(0, 2)
    assert pot.round_done()

def test_pot_three_players_bad_end_round():
    pot = Pot(range(3))
    assert not pot.round_done()
    pot.receive_bet(0, 0) # Check
    assert not pot.round_done()
    pot.receive_bet(0, 1)
    try:
        pot.end_round()
    except PotException as e:
        assert str(e) == 'Betting round cannot be complete'
    else:
        assert False

def test_pot_skim_1():
    pot = Pot(range(3))
    pot.receive_bet(10, 0)
    pot.receive_bet(10, 1)
    assert pot.round_bets == {0: 10, 1: 10, 2: None}
    assert pot.chips == 0
    for_next_pot = pot.skim_for_side_pot(7)
    assert pot.round_bets == {0: 7, 1: 7, 2: None}
    assert for_next_pot == {0: 3, 1: 3, 2: None}

def test_pot_skim_2():
    pot = Pot(range(3))
    pot.receive_bet(5, 0)
    pot.receive_bet(10, 1)
    assert pot.round_bets == {0: 5, 1: 10, 2: None}
    assert pot.chips == 0
    for_next_pot = pot.skim_for_side_pot(7)
    assert pot.round_bets == {0: 5, 1: 7, 2: None}
    assert for_next_pot == {1: 3, 2: None}

def test_pot_starting_chips():
    pot = Pot(range(1), 10)
    assert pot.round_bets == {0: None}
    assert pot.chips == 10

def test_pot_initial_round_bets():
    pot = Pot(range(3), initial_round_bets={0: 5, 2: 5})
    assert pot.chips == 0
    assert pot.round_bets == {0: 5, 2: 5}

def test_pot_initial_round_bets_chained():
    pot = Pot(range(3))
    pot.receive_bet(15, 0)
    pot2 = Pot(range(3), initial_round_bets=pot.skim_for_side_pot(10))
    assert pot.chips == 0
    assert pot.round_bets == {0: 10, 1: None, 2: None}
    assert pot2.chips == 0
    print pot2.round_bets
    assert pot2.round_bets == {0: 5, 1: None, 2: None}

def test_pot_action_needed():
    pot = Pot(range(3))
    assert pot.action_needed(0)
    assert pot.action_needed(1)
    assert pot.action_needed(2)
    assert not pot.action_needed(3)
    pot.receive_bet(10, 0)
    assert not pot.action_needed(0)
    assert pot.action_needed(1)
    assert pot.action_needed(2)
    pot.receive_bet(20, 1) # a raise
    assert pot.action_needed(0)
    assert not pot.action_needed(1)
    assert pot.action_needed(2)

