value_map = {
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}
value_map.update(dict([reversed(i) for i in value_map.items()]))

class Card(object):
    def __init__(self, suit=None, value=None):
        self.suit = suit
        if isinstance(value, basestring):
            if value.isdigit():
                value = int(value)
            else:
                value = value_map[value]
        self.value = value

    def cmp_value(self, other):
        print 'CMPV', self, other
        return cmp(self.value, other.value)
        
    def __str__(self):
        return '{0}{1}'.format(value_map[self.value] if self.value > 10 else str(self.value), self.suit)

    def __repr__(self):
        return '<Card {0}>'.format(self.__str__())

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
