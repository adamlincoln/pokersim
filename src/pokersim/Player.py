from Decision import Decision

class Player(object):
    def __init__(self, chips):
        self.chips = chips
        self.leave()
        self.discard_hole_cards()

    def sit(self, table, position):
        self.table = table
        self.position = position
        table.players[position] = self

    def leave(self):
        self.table = None
        self.position = None

    def discard_hole_cards(self):
        self.hole_cards = []

    def __repr__(self):
        return '<Player Pos: {0}  Hole Cards: {1}  Chips: {2}>'.format(
            str(self.position) if self.position != None else '',
            ', '.join([repr(card) for card in self.hole_cards]),
            str(self.chips)
        )

    def decide(self, error=None, force=None):
        if force is not None:
            return force
        return Decision.FOLD
