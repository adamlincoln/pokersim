from ChipPile import ChipPile

class Pot(object):
    def __init__(self, eligible_to_win, chips=0, initial_round_bets=None):
        if initial_round_bets is not None:
            self.round_bets = initial_round_bets
        else:
            self.round_bets = self.new_round(eligible_to_win)
        self._chippile = ChipPile('Pot', chips)

    @property
    def chips(self):
        return self._chippile.chips

    @chips.setter
    def chips(self, value):
        if isinstance(value, int):
            self._chippile.chips = value
        elif isinstance(value, ChipPile):
            self._chippile.chips = value.chips

    @staticmethod
    def new_round(eligible_to_win):
        return dict(zip(eligible_to_win, [None for pos in eligible_to_win]))

    def action_needed(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is None:
                return True
            elif self.round_bets[position].chips < max([pile.chips for pile in self.round_bets.values() if pile is not None]):
                return True
        else:
            return False

    def round_done(self):
        if None in self.round_bets.values():
            return False
        if len(set([pile.chips for pile in self.round_bets.values()])) > 1:
            return False
        return True

    def end_round(self):
        if self.round_done():
            for pile in self.round_bets.values():
                # Do I need to be subtracting from the round_bets values here too for tracking?
                # Yes! Conduit from round_bets value to self.chips.
                self.chips += pile.chips
            self.round_bets = self.new_round(self.round_bets.keys())
        else:
            raise PotException('Betting round cannot be complete')

    def receive_bet(self, amt, frm):
        if frm not in self.round_bets:
            raise PotException('Position {0} is not eligible to win'.format(str(frm)))
        if self.round_bets[frm] is not None:
            self.round_bets[frm].chips += amt
        else:
            self.round_bets[frm] = ChipPile('Pot Round Bet for {0}'.format(frm), amt)

    def skim_for_side_pot(self, skim_to_amt):
        for_new_side_pot = {}
        for position, pile in self.round_bets.iteritems():
            if pile is None:
                for_new_side_pot[position] = None
            else:
                if skim_to_amt < pile.chips:
                    for_new_side_pot[position] = ChipPile('Skim for side pot', pile.chips - skim_to_amt)
                    self.round_bets[position].chips = skim_to_amt
        return for_new_side_pot

    def make_ineligible_to_win(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is not None:
                self.chips += self.round_bets[position].chips
            del self.round_bets[position]
        else:
            raise PotException('Position {0} is already not eligible to win'.format(position))

class PotException(Exception):
    pass
