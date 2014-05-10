class Pot(object):
    def __init__(self, eligible_to_win, chips=0, initial_round_bets=None):
        self.eligible_to_win = eligible_to_win 
        self.chips = chips
        if round_bets is not None:
            self.round_bets = initial_round_bets
            #assert self.positions_eligible_to_win() # What is this for??

    def positions_eligible_to_win(self):
        return [player.position for player in self.eligible_to_win]

    def new_round(self):
        #self.round_bets = dict([(player.position, None) for player in self.eligible_to_win])
        positions = self.positions_eligible_to_win()
        self.round_bets = dict(zip(positions, [None for pos in positions]))

    def round_done(self):
        if None in self.round_bets.values():
            return False
        if len(set(self.round_bets.values())) > 1:
            return False
        return True

    def end_round(self):
        for amt in self.round_bets.values():
            self.chips += amt
        del self.round_bets

    def receive_bet(self, frm, amt):
        assert frm in self.positions_eligible_to_win()
        self.round_bets[frm] = self.round_bets[frm] + amt if self.round_bets[frm] is not None else amt

    def skim_for_side_pot(self, skim_to_amt):
        for_new_side_pot = {}
        for position, amt in self.round_bets.iteritems():
            if amt is not None and skim_to_amt < amt:
                for_new_side_pot[position] = amt - skim_to_amt
                self.round_bets[position] = skim_to_amt
        return for_new_side_pot

    def make_ineligible_to_win(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is not None:
                self.chips += self.round_bets[position]
                del self.round_bets[position]
        # Remove from self.eligible_to_win, yes?

