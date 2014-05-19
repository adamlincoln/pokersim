from pubsub import pub

from Deck import Deck
from Player import Player
from Decision import Decision
from Pot import Pot

class Table(object):
    '''This is essentially the House.  It runs the game.'''
    def __init__(self):
        # self.players is going to be a dict with ints as keys denoting the seats each player has.
        self.players = {}
        self.button_seat = -1
        self.rake = 0
        self.tips = 0
        self.units = [2, 2, 4, 4]
        self.limits = [10, 10, 20, 20]
        self.action = None

    def initialize_hand(self):
        self.move_button()
        self.pots = [Pot(self.players.keys())]
        self.action = self.button_seat
        self.deck = Deck()
        self.deck.shuffle()
        for position, player in self.players.iteritems():
            player.discard_hole_cards()
        self.board = []

    def take_blinds(self):
        self.take_bet(1)
        self.incr_action()
        self.take_bet(2)

    def burn_one_card(self):
        return self.deck.deal()

    def deal_one_hole_card_to_all_players(self):
        # I'm not 100% happy with this, but it works.
        while True:
            self.incr_action()
            self.players[self.action].hole_cards.append(self.deck.deal())
            if self.action == self.button_seat:
                break

    def deal_one_community_card(self):
        self.board.append(self.deck.deal())

    def flop(self):
        self.burn_one_card()
        for i in xrange(3):
            self.deal_one_community_card()

    def turn(self):
        self.burn_one_card()
        self.deal_one_community_card()

    def river(self):
        self.turn()

    def pots_need_action(self, position):
        for pot in self.pots:
            if pot.action_needed(position):
                return True
        return False

    def run_betting_round(self):
        last_to_act = None
        while self.action != last_to_act:
            if self.pots_need_action(self.action):
                error = None
                decision = self.players[self.action].decide(error)
                if decision == Decision.FOLD:
                    for pot in self.pots:
                        pot.make_ineligible_to_win(self.action)
                elif decision == Decision.CHECK:
                    pass
                elif decision == Decision.CALL:
                    # Remember that if you skim for a side pot, you have to effectively fold the current action out of any new side pot you make
                    pass
                elif decision == Decision.RAISE:
                    pass
            potential_winner = self.look_for_winner()
            if potential_winner is not None:
                for pot in self.pots:
                    pot.end_round()
                return potential_winner
            last_to_act = self.action
            self.incr_action()
        for pot in self.pots:
            pot.end_round()

    def look_for_winner(self):
        # check for one player left - winner!
        #winner = self.round_pot.keys()[0] if len(self.round_pot) == 1 else None
        potential_winner = None
        for pot in self.pots:
            if len(pot.round_bets) == 1:
                if potential_winner is None:
                    potential_winner = pot.round_bets.keys()[0]
                else:
                    if potential_winner != pot.round_bets.key()[0]: # Check for bad data state
                        raise TableException('Bad data state in single player pots')
        return potential_winner

    def determine_final_winners(self):
        pass

    def pay(self, position, amt):
        self.players[position].chips += amt

    def end_hand(self, winners):
        #individ_winnings = None
        if len(winners) != len(self.pots):
            raise TableException('Hand ending with non-matching numbers of winners and pots.')
        for pot in self.pots:
            if set(pot.round_bets.values()) != set([None]):
                raise TableException('Hand ending with at least one pot that\'s not ready.')
        winnings = []
        for potnum in xrange(len(self.pots)):
            pot_winnings = {}
            extra_winnings = self.pots[potnum].chips % len(winners[potnum])
            if extra_winnings == 0:
                for winner in winners[potnum]:
                    pot_winnings[winner] = self.pots[potnum].chips / len(winners[potnum])
                #individ_winnings = self.pot / len(winners)
            else:
                equal_share = (self.pots[potnum].chips - extra_winnings) / len(winners[potnum])
                for winner in winners[potnum]:
                    pot_winnings[winner] = equal_share
                player = self.button_seat
                while True:
                    player = self.next_player_position(player)
                    if player in winners[potnum]:
                        pot_winnings[player] += extra_winnings
                        #self.players[player].chips += extra_winnings
                        #self.pay(self.players[player], extra_winnings)
                        break
                #individ_winnings = (self.pot - extra_winnings) / len(winners)
                #player = self.next_player_position(self.button_seat)
                #while True:
                    #if player in winners:
                        ##self.players[player].chips += extra_winnings
                        #self.pay(self.players[player], extra_winnings)
                        #break
                    #player = self.next_player_position(player)
            winnings.insert(0, pot_winnings)
            #for winner in winners:
                ##self.players[winner].chips += individ_winnings
                #self.pay(self.players[winner], individ_winnings)

        for potnum in xrange(len(winnings)):
            pot_winnings = winnings[potnum]
            for player, amt in pot_winnings.iteritems():
                self.pots[potnum].chips -= amt
                self.pay(player, amt)
            if self.pots[potnum].chips != 0:
                raise TableException('Problem paying hand.')

        #self.pot = 0
        #self.side_pot = 0
        #self.round_pot = {}
        #self.round_side_pots = {}
        #for player in self.players:
            #del player.hole_cards[:]
        #self.move_button()

    def deal(self):
        self.initialize_hand()
        # Deal first two cards first, so I can use self.action to make it simpler.
        self.burn_one_card()
        self.deal_one_hole_card_to_all_players()
        self.deal_one_hole_card_to_all_players()

        # Get blinds
        self.incr_action()
        self.take_blinds()
        self.incr_action()
        error = None

        # ROUND ONE - FIGHT
        # Is this too loopy? internally even
        # What really happens: action moves.  if the player at action is in any pot, he makes ONE decision.  This deterimnes his standing in ALL pots.
        hand_done = False
        winner = self.run_betting_round()
        while True: # This isn't really a loop, but an ugly GOTO.  Is there a better way to do this?
            if winner is not None:
                self.end_hand([[winner] for pot in self.pots])
                hand_done = True
                break
            self.flop()
            winner = self.run_betting_round()
            if winner is not None:
                self.end_hand([[winner] for pot in self.pots])
                hand_done = True
                break
            self.turn()
            winner = self.run_betting_round()
            if winner is not None:
                self.end_hand([[winner] for pot in self.pots])
                hand_done = True
                break
            self.river()
            winner = self.run_betting_round()
            if winner is not None:
                self.end_hand([[winner] for pot in self.pots])
                hand_done = True
            break

        if not hand_done:
            winners = self.determine_final_winners()
            self.end_hand(winners)

        blah = '''while not (len(set(self.round_pot.values())) == 1 and set(self.round_pot.values()).pop() is not None):
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
        '''
        # Flop
        # Round Two
        # Turn
        # Round Three
        # River
        # Round Four
        # Determine winner
        # Pay the winner (winner tips)

    def current_bet_amt(self):
        return max(self.round_pot.values())

    def next_bet_amt(self, betting_round):
        return self.current_bet_amt + self.unit[betting_round]

    def at_limit(self, betting_round):
        return False if self.next_bet_amt(betting_round) <= self.limits[betting_round] else True

    def next_player_position(self, pos):
        positions_filled = self.players.keys()
        positions_filled.sort()
        for position_filled in positions_filled:
            if position_filled > pos:
                return position_filled
        return positions_filled[0]
        #if pos >= len(self.players) - 1:
            #return 0
        #else:
            #return pos + 1

    def incr_action(self):
        if self.action is None:
            raise TableException('Hand not initialized')
        #print 'action moving from player', self.action
        while True:
            potential_action = self.next_player_position(self.action)
            for pot in self.pots:
                if pot.action_needed(potential_action):
                    self.action = potential_action
                    #print 'to player', self.action
                    return
        raise TableException('Action not incremented from {0}'.format(self.action))

    def take_bet(self, amt):
        '''A nuance here is that the creation of a side pot is triggered when this gets called with amt > the player's available chips.'''
        for potnum in xrange(len(self.pots)):
            if potnum == len(self.pots) - 1:
                if self.players[self.action].chips >= amt:
                    self.players[self.action].chips -= amt
                    self.pots[potnum].receive_bet(self.action, amt)
                    pub.sendMessage('bet', data={'potnum': potnum, 'who': self.action, 'amt': amt})
                elif self.players[self.action].chips > 0:
                    self.pots[potnum].receive_bet(self.action, self.players[self.action].chips)
                    pub.sendMessage('bet', data={'potnum': potnum, 'who': self.action, 'amt': self.players[self.action].chips})
                    for_side_pot = self.pots[potnum].skim_for_side_pot(self.players[self.action].chips)
                    self.pots.append(Pot(for_side_pot.keys(), initial_round_bets=for_side_pot))
                    self.players[self.action].chips = 0
            else:
                if self.players[self.action].chips >= max(self.pots[potnum].round_bets.values()):
                    self.players[self.action].chips -= max(self.pots[potnum].round_bets.values())
                    pub.sendMessage('bet', data={'potnum': potnum, 'who': self.action, 'amt': max(self.pots[potnum].round_bets.values())})
                    self.pots[potnum].receive_bet(self.action, max(self.pots[potnum].round_bets.values()))
                    amt -= max(self.pots[potnum].round_bets.values())
                elif self.players[self.action].chips > 0:
                    self.pots[potnum].receive_bet(self.action, self.players[self.action].chips)
                    pub.sendMessage('bet', data={'potnum': potnum, 'who': self.action, 'amt': self.players[self.action].chips})
                    for_side_pot = self.pots[potnum].skim_for_side_pot(self.players[self.action].chips)
                    for pot in self.pots[potnum + 1:]:
                        pot.make_ineligible_to_win(self.action)
                    self.pots.insert(potnum + 1, Pot(for_side_pot.keys(), initial_round_bets=for_side_pot))
                    self.players[self.action].chips = 0
                    break # Nothing left!

    def move_button(self):
        self.button_seat = self.next_player_position(self.button_seat)

class TableException(Exception):
    pass
