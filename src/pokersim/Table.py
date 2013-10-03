from Deck import Deck
from Player import Player
from Decision import Decision

class Table(object):
    '''This is essentially the House.  It runs the game.'''
    def __init__(self, num_players=10):
        self.players = [Player(self, i) for i in xrange(num_players)]
        self.button_seat = 0
        self.rake = 0
        self.tips = 0
        self.pot = 0
        self.side_pot = 0
        self.round_pot = {}
        self.round_side_pot = {}
        self.action = 0
        self.players_eligible_for_action = []
        self.board = []

    def deal(self):
        assert(self.pot == 0)
        assert(self.side_pot == 0)
        assert(self.round_pot == {})
        assert(self.round_side_pot == {})
        deck = Deck()
        deck.shuffle()
        self.players_eligible_for_action = [i for i in len(self.players)]
        # Deal first two cards first, so I can use self.action to make it simpler.
        #self.action = self.next_player_position(self.button_seat)
        self.action = self.button_seat
        while True:
            self.incr_action()
            self.players[self.action].hole_cards.append(deck.deal())
            if self.action == self.button_seat:
                break
        while True:
            self.incr_action()
            self.players[self.action].hole_cards.append(deck.deal())
            if self.action == self.button_seat:
                break
        # Round One (at any point, rake)
        # Get blinds
        self.incr_action()
        self.take_blind(self.action, 1)
        self.incr_action()
        self.take_blind(self.action, 2)
        self.incr_action()
        decision = self.players[self.action].decide()
        if decision == Decision.FOLD:
            self.players_eligible_for_action.remove(self.action)
            del self.players[self.action].cards[:]
        elif decision == Decision.CHECK:
        elif decision == Decision.CALL:
        elif decision == Decision.RAISE:

        print self.players
        # Flop
        # Round Two
        # Turn
        # Round Three
        # River
        # Round Four
        # Determine winner
        # Pay the winner (winner tips)
        self.move_button()

    def next_player_position(self, pos):
        if pos >= len(self.players) - 1:
            return 0
        else:
            return pos + 1

    def incr_action(self):
        print 'action moving from player', self.action
        while True:
            self.action = self.next_player_position(self.action)
            if self.action in self.players_eligible_for_action:
                break
        print 'to player', self.action

    def take_blind(self, pos, amt):
        self.players[pos].chips -= amt
        self.round_pot[pos] = amt

    def move_button(self):
        self.button_seat = self.next_player_position(self.button_seat)
