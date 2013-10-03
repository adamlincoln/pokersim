class Card:
    def __init__(self, suit=None, value=None):
        self.suit = suit
        self.value = value

    def __str__(self):
        return '{0}{1}'.format(self.value, self.suit)

    def __repr__(self):
        return '<Card {0}'.format(self.__str__())
