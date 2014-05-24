from itertools import groupby
from itertools import chain

from Card import Card

hand_rank = {
    8: 'Straight flush',
    7: 'Four of a kind',
    6: 'Full house',
    5: 'Flush',
    4: 'Straight',
    3: 'Three of a kind',
    2: 'Two pair',
    1: 'Pair',
    0: 'High card'
}

class Hand(object):
    def __init__(self, cards):
        self.cards = cards

    def rank(self):
        # Can this be cached somehow?

        hand = self.cards # Erm, for ease of reading?

        hand.sort(cmp = Card.cmp_value)
        # First, I need this a lot, so do it once
        hand_values = [card.value for card in hand]

        # Look for straight
        straight = True
        for i in xrange(len(hand_values) - 1):
            l, r = hand_values[i:i + 2]
            if r - l != 1:
                straight = False
                break
        if hand_values == [2, 3, 4, 5, 14]: # accounts for ace low
            straight = True

        # Look for flush
        flush = False
        if len(set([card.suit for card in hand])) == 1:
            flush = True

        if straight:
            value = hand_values[4]
            if value == 14 and hand_values[0] == 2:
                value = 5 # accounts for ace low
            if flush:
                # Straight flush?
                return {'rank': 8, 'values': [value]}
            else:
                # Straight?
                return {'rank': 4, 'values': [value]}

        if flush:
            # Flush?
            return {'rank': 5, 'values': list(reversed(hand_values))}

        # Look for multiples
        multiples = {}
        for hand_value, hand_value_iter in groupby(hand_values):
            num = len(list(hand_value_iter))
            if num in multiples:
                multiples[num].append(hand_value)
            else:
                multiples[num] = [hand_value]
        # Four of a kind?
        if 4 in multiples:
            return {'rank': 7, 'values': [multiples[4][0], multiples[1][0]]}
        # Full house?
        if 3 in multiples and 2 in multiples:
            return {'rank': 6, 'values': [multiples[3][0], multiples[2][0]]}
        # Three of a kind?
        if 3 in multiples:
            return {'rank': 3, 'values': chain.from_iterable([multiples[3], reversed(multiples[1])])}
        if 2 in multiples:
            # Two pair?
            if len(multiples[2]) == 2:
                return {'rank': 2, 'values': chain.from_iterable([reversed(multiples[2]), multiples[1]])}
            # Pair?
            if len(multiples[2]) == 1:
                return {'rank': 1, 'values': chain.from_iterable([multiples[2], reversed(multiples[1])])}
        # High card
        return {'rank': 0, 'values': chain.from_iterable([reversed(multiples[1])])}

    def __cmp__(self, other):
        #if not hasattr(self, 'cached_rank'):
        self.cached_rank = self.rank()
        #if not hasattr(other, 'cached_rank'):
        other.cached_rank = other.rank()
        if self.cached_rank['rank'] < other.cached_rank['rank']:
            return -1
        elif self.cached_rank['rank'] > other.cached_rank['rank']:
            return 1
        else:
            self_tiebreakers = list(self.cached_rank['values'])
            other_tiebreakers = list(other.cached_rank['values'])
            for i in xrange(len(self_tiebreakers)): # Kickers
                if self_tiebreakers[i] < other_tiebreakers[i]:
                    return -1
                elif self_tiebreakers[i] > other_tiebreakers[i]:
                    return 1

        return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0
