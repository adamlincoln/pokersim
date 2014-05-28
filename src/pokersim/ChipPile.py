class ChipPile(object):
    def __init__(self, name, chips=0):
        self.name = name
        self.chips = chips

    def __str__(self):
        return '{0}: {1}'.format(self.name, str(self.chips))

    def __repr__(self):
        return '<ChipPile {0} >'.format(str(self))

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.chips == other.chips
