from Decision import Decision

class Player(object):
    def __init__(self, table, position):
        self.chips = 100
        self.table = table
        self.position = position
        self.hole_cards = []

    def __repr__(self):
        return '<Player Pos: {0}  Hole Cards: {1}  Chips: {2}>'.format(
            str(self.position) if hasattr(self, 'position') and self.position != None else '',
            str(self.hole_cards),
            str(self.chips)
        )

    def decide(self, error, force=None):
        if force is not None:
            return force
        return Decision.FOLD
