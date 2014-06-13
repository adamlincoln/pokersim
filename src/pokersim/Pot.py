from ChipConduit import ChipConduit

class Pot(object):
    def __init__(self, eligible_to_win, chips=[], initial_round_bets=None):
        if initial_round_bets is not None:
            self.round_bets = initial_round_bets
        else:
            self.round_bets = self.new_round(eligible_to_win)
        print 'CHIPS', eligible_to_win, chips, initial_round_bets
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
        #if len(set(self.round_bets.values())) > 1:
        if len(set([len(value) for value in self.round_bets.values()])) > 1:
            return False
        return True

    def end_round(self):
        print 'WHATWHAT'
        if self.round_done():
            for position, chips in self.round_bets.iteritems():
                ChipConduit.move(len(chips), self.round_bets, position, self, 'chips') # Untracked right now
            self.round_bets = self.new_round(self.round_bets.keys())
        else:
            raise PotException('Betting round cannot be complete')

    def receive_bet(self, amt, frm, skim=False):
        if frm.position not in self.round_bets:
            raise PotException('Position {0} is not eligible to win'.format(str(frm.position)))
        move_kwargs = {
            'frm_tracking': {
                'type': 'player',
                'position': frm.position,
                'brain': frm.brain.__class__.__name__
            },
            'to_tracking': 'pot',
        }
        if skim:
            move_kwargs = {
                'between': self.skim_for_side_pot,
                'between_args': [len(frm.chips)],
            }
        print 'AMT', amt
        print 'SCs', len(self.chips)
        #print frm
        #print frm.chips
        print 'RBS', self.round_bets
        print 'POS', frm.position
        return ChipConduit.move(
            amt,
            frm,
            'chips',
            self.round_bets,
            frm.position,
            **move_kwargs
        )

    def skim_for_side_pot(self, skim_to_amt):
        for_new_side_pot = {}
        for position, chips in self.round_bets.iteritems():
            if chips is None:
                for_new_side_pot[position] = None
            else:
                if skim_to_amt < chips:
                    for_new_side_pot[position] = chips[skim_to_amt:]
                    self.round_bets[position] = chips[:skim_to_amt]
        return for_new_side_pot, {'amt': skim_to_amt}

    def make_ineligible_to_win(self, position):
        if position in self.round_bets:
            if self.round_bets[position] is not None:
                ChipConduit.move(len(self.round_bets[position]), self.round_bets, position, self, 'chips') # Untracked right now
            del self.round_bets[position]
        else:
            raise PotException('Position {0} is already not eligible to win'.format(position))

class PotException(Exception):
    pass
