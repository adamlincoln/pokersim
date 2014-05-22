import simplejson as json
import random

from Card import Card

class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in ('D', 'H', 'S', 'C'):
            for value in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'):
                self.cards.append(Card(suit = suit, value = value))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return json.dumps([str(card) for card in self.cards])

    def deal(self, n=1):
        if n == 1:
            if len(self.cards) > 0:
                return self.cards.pop(0)
            else:
                raise IndexError('No cards left in deck')
        else:
            return [self.deal() for i in xrange(n)]
