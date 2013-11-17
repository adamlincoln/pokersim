from pubsub import pub

from Deck import Deck
from Player import Player
from Decision import Decision
from Pot import Pot

class Table(object):
    '''This is essentially the House.  It runs the game.'''
    def __init__(self, num_players=10):
        self.players = [Player(self, i) for i in xrange(num_players)]
        self.button_seat = 0
        self.rake = 0
        self.tips = 0
        self.units = [2, 2, 4, 4]
        self.limits = [10, 10, 20, 20]

    def initialize_hand(self):
        #self.pot = {tuple(range(len(self.players))): 0}
        self.pots = [Pot(self.players)]
        #self.side_pot = 0
        #self.round_pot = {}
        #self.round_pot = dict([(i, None) for i in xrange(len(self.players))])
        #self.round_side_pots = {}
        #self.round_side_pots = dict([(i, None) for i in xrange(len(self.players))])
        #self.round_side_pots = {}
        self.action = self.button_seat
        #self.players_eligible_for_action = [i for i in xrange(len(self.players))]
        self.board = []

    def deal(self):
        self.initialize_hand()
        #assert(self.pot == {})
        #assert(self.side_pot == 0)
        #assert(self.round_pot == {})
        #assert(self.round_side_pots == {})
        deck = Deck()
        deck.shuffle()
        # Deal first two cards first, so I can use self.action to make it simpler.
        #self.action = self.next_player_position(self.button_seat)
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
        self.take_bet(1)
        self.take_bet(2)
        error = None
        while not (len(set(self.round_pot.values())) == 1 and set(self.round_pot.values()).pop() is not None):
            while True:
                decision = self.players[self.action].decide(error)
                if decision == Decision.FOLD:
                    self.players_eligible_for_action.remove(self.action)
                    self.pot += self.round_pot[self.action] if self.round_pot[self.action] is not None else 0
                    del self.round_pot[self.action]
                    del self.players[self.action].hole_cards[:]
                    self.incr_action()
                    break
                #elif decision == Decision.CHECK:
                    ## If first to act or everyone else who has acted has checked
                    #if max(self.round_pot.values()) == None or max(self.round_pot.values()) == 0:
                        #self.take_bet(0)
                        #break
                    #else:
                        #allowed_decisions = [Decision.CALL, Decision.FOLD]
                        #if not self.at_limit(0):
                            #allowed_decisions.append(Decision.RAISE)
                        #error = {'allowed_decisions': allowed_decisions}
                elif decision == Decision.CALL: # CALL is the same as check if first to act (no other bets made)
                    if self.current_bet_amt() is None:
                        self.take_bet(0)
                    else: 
                        self.take_bet(max(self.round_pot.values()))
                    break
                elif decision == Decision.RAISE: # RAISE is the same as 'bet' if first to act or following only checks
                    if not self.at_limit(0):
                        self.take_bet(self.next_bet_amt(0))
                        break
                    else:
                        error = {'allowed_decisions': [Decision.CALL, Decision.FOLD]}
        # check for one player left - winner!
        winner = self.round_pot.keys()[0] if len(self.round_pot) == 1 else None
        # move round_pot to pot
        # clear round_pot
        for seat in self.round_pot.keys():
            self.pot += self.round_pot[seat]
            del self.round_pot[seat]

        if winner:
            self.end_hand([winner])

        print self.players
        # Flop
        # Round Two
        # Turn
        # Round Three
        # River
        # Round Four
        # Determine winner
        # Pay the winner (winner tips)

    def end_hand(self, winners):
        print 'END HAND. WINNERS:', [self.players[player] for player in winners]
        individ_winnings = None
        if self.pot % len(winners) == 0:
            individ_winnings = self.pot / len(winners)
        else:
            extra_winnings = self.pot % len(winners)
            individ_winnings = (self.pot - extra_winnings) / len(winners)
            player = self.next_player_position(self.button_seat)
            while True:
                if player in winners:
                    #self.players[player].chips += extra_winnings
                    self.pay(self.players[player], extra_winnings)
                    break
                player = self.next_player_position(player)
        for winner in winners:
            #self.players[winner].chips += individ_winnings
            self.pay(self.players[winner], individ_winnings)

        self.pot = 0
        self.side_pot = 0
        self.round_pot = {}
        self.round_side_pots = {}
        for player in self.players:
            del player.hole_cards[:]
        self.move_button()

    @staticmethod
    def pay(player, amt):
        print 'PAYING', amt, 'CHIPS TO PLAYER', player
        player.chips += amt

    def current_bet_amt(self):
        return max(self.round_pot.values())

    def next_bet_amt(self, betting_round):
        return self.current_bet_amt + self.unit[betting_round]

    def at_limit(self, betting_round):
        return False if self.next_bet_amt(betting_round) <= self.limits[betting_round] else True

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

    def take_bet(self, amt):
        if self.players[self.action].chips >= amt:
            self.players[self.action].chips -= amt
            self.pots[-1].receive_bet(amt)
            #self.round_pot[self.action] = amt
            pub.sendMessage('bet', who = self.action, amt = amt)
            self.incr_action()
        else:
            self.round_pot[self.action] = self.players[self.action].chips
            for seat, bet in self.round_pot.iteritems():
                self.round_side_pots[self.action] = {} # How to denote a side pot and who is out of it?  For future betting, for payouts, determining winner...
                self.round_side_pots[self.action][seat] = bet - self.round_pot[self.action]
                self.round_pot[seat] = self.round_pot[self.action]

    def move_button(self):
        self.button_seat = self.next_player_position(self.button_seat)
