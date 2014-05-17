class Pot(object):
    def __init__(self, eligible_to_win, chips=0, initial_round_bets=None):
        if initial_round_bets is not None:
            self.round_bets = initial_round_bets
        else:
            self.round_bets = self.new_round(eligible_to_win)
        self.chips = chips

    @staticmethod
    def new_round(eligible_to_win):
        return dict(zip(eligible_to_win, [None for pos in eligible_to_win]))

    def action_needed(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is None:
                return True
            elif self.round_bets[position] < max(self.round_bets.values()):
                return True
        else:
            return False

    def round_done(self):
        if None in self.round_bets.values():
            return False
        if len(set(self.round_bets.values())) > 1:
            return False
        return True

    def end_round(self):
        if self.round_done():
            for amt in self.round_bets.values():
                self.chips += amt
            self.round_bets = self.new_round(self.round_bets.keys())
        else:
            raise PotException('Betting round cannot be complete')

    def receive_bet(self, frm, amt):
        if frm not in self.round_bets:
            raise PotException('Position {0} is not eligible to win'.format(str(frm)))
        self.round_bets[frm] = self.round_bets[frm] + amt if self.round_bets[frm] is not None else amt

    def skim_for_side_pot(self, skim_to_amt):
        for_new_side_pot = {}
        for position, amt in self.round_bets.iteritems():
            if amt is None:
                for_new_side_pot[position] = None
            else:
                if skim_to_amt < amt:
                    for_new_side_pot[position] = amt - skim_to_amt
                    self.round_bets[position] = skim_to_amt
        return for_new_side_pot

    def make_ineligible_to_win(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is not None:
                self.chips += self.round_bets[position]
            del self.round_bets[position]
        else:
            raise PotException('Position {0} is already not eligible to win'.format(position))

class PotException(Exception):
    pass
