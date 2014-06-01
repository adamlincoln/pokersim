from pokersim.Table import Table
from pokersim.Table import TableException
from pokersim.Player import Player

def test_table_defaults():
    table = Table()
    assert table.players == {}
    assert table.button_seat == -1
    assert table.rake == 0
    assert table.tips == 0
    assert table.units == [2, 2, 4, 4]
    assert table.limits == [10, 10, 20, 20]
    assert table.action is None

def test_table():
    table = Table()
    for i in xrange(3):
        player = Player(10)
        player.sit(table, i)
    table.initialize_hand()
    assert table.board == []
    assert table.button_seat == 0
    assert table.action == 0
    assert len(table.pots) == 1
    assert table.pots[0].chips == 0
    assert table.pots[0].round_bets == {0: None, 1: None, 2: None}

def test_table_no_initialize():
    table = Table()
    for i in xrange(3):
        player = Player(10)
        player.sit(table, i)
    try:
        table.deal_one_hole_card_to_all_players()
    except TableException as e:
        assert str(e) == 'Hand not initialized'
    else:
        assert False

def test_table_deal_hole_card():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    to_burn = table.deck.cards[0]
    player_cards = [[table.deck.cards[i+1]] for i in xrange(num_players)]
    assert to_burn == table.burn_one_card()
    table.deal_one_hole_card_to_all_players()
    for i in xrange(1, num_players):
        assert players[i].hole_cards == player_cards[i-1]
    assert players[0].hole_cards == player_cards[-1]

def test_table_deal_two_hole_cards():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    to_burn = table.deck.cards[0]
    player_cards = [[table.deck.cards[i+1], table.deck.cards[i+1+num_players]] for i in xrange(num_players)]
    assert to_burn == table.burn_one_card()
    table.deal_one_hole_card_to_all_players()
    table.deal_one_hole_card_to_all_players()
    for i in xrange(1, num_players):
        assert players[i].hole_cards == player_cards[i-1]
    assert players[0].hole_cards == player_cards[-1]
    assert table.action == 0

def test_table_take_blinds():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    table.incr_action()
    table.take_blinds()
    # This will have to change when I support more types of games
    assert table.pots[0].round_bets == {1: 1, 2: 2, 0: None}
    assert table.action == 2

def test_table_community_card():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    remember = table.deck.cards[0]
    table.deal_one_community_card()
    assert table.board == [remember]

def test_table_flop():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    to_burn = table.deck.cards[0]
    board_cards = table.deck.cards[1:4]
    table.flop()
    assert table.board == board_cards

def test_table_turn():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    to_burn = table.deck.cards[0]
    remember = table.deck.cards[1]
    table.turn()
    assert table.board == [remember]

def test_table_river():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    to_burn = table.deck.cards[0]
    remember = table.deck.cards[1]
    table.river()
    assert table.board == [remember]

def test_table_pots_need_action():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    table.incr_action()
    table.take_blinds()
    assert table.pots_need_action(0)
    assert table.pots_need_action(1)
    assert not table.pots_need_action(2)

def test_table_run_betting_round():
    table = Table()
    # Dealer will bet first preflop, so 2 will win as for now all players will fold
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    table.incr_action()
    table.take_blinds()
    winner = table.run_betting_round()
    assert winner == 2
    assert len(table.pots) == 1
    assert table.pots[0].chips == 3 # For a 1/2 limit game

def test_table_end_hand_via_fold():
    table = Table()
    # Dealer will bet first preflop, so 2 will win as for now all players will fold
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    table.incr_action()
    table.take_blinds()
    winner = table.run_betting_round()
    assert winner == 2
    assert len(table.pots) == 1
    assert table.pots[0].chips == 3 # For a 1/2 limit game
    table.end_hand([[winner]])
    assert players[0].chips == 10
    assert players[1].chips == 9
    assert players[2].chips == 11

def test_table_take_bet_skim():
    table = Table()
    player = Player(4)
    player.sit(table, 0)
    for i in (1, 2):
        player = Player(10)
        player.sit(table, i)

    table.initialize_hand()
    table.incr_action()
    table.take_bet(5)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: 6}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 2
    assert table.pots[0].round_bets == {1: 4, 0: 4, 2: 4}
    assert table.pots[1].round_bets == {1: 1, 2: 2}
    assert table.players[0].chips == 0
    assert table.players[1].chips == 5
    assert table.players[2].chips == 4

def test_table_take_bet_skim_bet_after():
    table = Table()
    player = Player(4)
    player.sit(table, 3)
    for i in (0, 1, 2):
        player = Player(10)
        player.sit(table, i)

    table.initialize_hand()
    table.incr_action()
    table.take_bet(5)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: None, 3: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: 6, 3: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 2
    assert table.pots[0].round_bets == {1: 4, 0: None, 2: 4, 3: 4}
    assert table.pots[1].round_bets == {1: 1, 2: 2, 0: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 2
    assert table.pots[0].round_bets == {1: 4, 0: 4, 2: 4, 3: 4}
    assert table.pots[1].round_bets == {1: 1, 2: 2, 0: 2}

def test_table_take_bet_two_skim_bets():
    table = Table()
    player = Player(3)
    player.sit(table, 0)
    player = Player(4)
    player.sit(table, 3)
    for i in (1, 2):
        player = Player(10)
        player.sit(table, i)

    table.initialize_hand()
    table.incr_action()
    table.take_bet(5)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: None, 3: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 1
    assert table.pots[0].round_bets == {1: 5, 0: None, 2: 6, 3: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 2
    assert table.pots[0].round_bets == {1: 4, 0: None, 2: 4, 3: 4}
    assert table.pots[1].round_bets == {1: 1, 2: 2, 0: None}
    table.incr_action()
    table.take_bet(6)
    assert len(table.pots) == 3
    assert table.pots[0].round_bets == {1: 3, 0: 3, 2: 3, 3: 3}
    assert table.pots[1].round_bets == {1: 1, 2: 1, 3: 1}
    assert table.pots[2].round_bets == {1: 1, 2: 2}

def test_table_deal_1():
    table = Table()
    # Dealer will bet first preflop, so 2 will win as for now all players will fold
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    assert table.button_seat == -1
    table.deal()
    assert table.button_seat == 0
    assert table.players[2].chips == 11
    assert table.players[1].chips == 9
    assert table.players[0].chips == 10

def test_table_determine_final_winner():
    table = Table()
    num_players = 3
    players = []
    for i in xrange(num_players):
        player = Player(10)
        player.sit(table, i)
        players.append(player)
    table.initialize_hand()
    table.deal_one_hole_card_to_all_players()
    table.deal_one_hole_card_to_all_players()
    table.flop()
    table.turn()
    table.river()

