class Player:
    def __init__(self, table, position):
        self.chips = 100
        self.table = table
        self.position = position
        self.hole_cards = []

    def __repr__(self):
        return '<Player Pos: {0}  Hole Cards: {1}>'.format(
            str(self.position) if hasattr(self, 'position') and self.position != None else '',
            str(self.hole_cards)
        )
